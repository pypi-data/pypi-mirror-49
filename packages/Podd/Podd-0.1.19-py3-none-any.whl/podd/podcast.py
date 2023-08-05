"""Define podcast & episode objects."""

import html
import re
import typing as tp
from http import client
from os import path
from ssl import CertificateError
from urllib.error import HTTPError, URLError

import feedparser as fp
import keyring
import mutagen
from keyring.errors import KeyringError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp4 import MP4
from requests import get
from requests.exceptions import ConnectionError

from podd.database import Database
from podd.logger import logger
from podd.utilities import compile_regex

# Some feeds send a silly amount of headers, crashing downloader; default is 100
client._MAXHEADERS = 1000
PATTERNS: tp.List[re.compile] = compile_regex()


class Podcast:
    """Define podcast model.

    Contains data about a specific podcast.

    JinjaPacket is used to organize episode and podcast info which helps when rendering
    the email notification message.  I'm using jinja2 to render the email messages,
    hence the name.
    """

    __slots__ = [
        "_url",
        "_dl_dir",
        "_logger",
        "_name",
        "_image",
        "_new_entries",
        "episodes",
        "headers",
    ]

    def __init__(self, url: str, directory: str, protected: bool):
        """init method.

        :param url: rss feed url for this podcast
        :param directory: download directory for this podcast
        """
        self._url = url
        self._dl_dir = directory
        self._logger = logger(f"{self.__class__.__name__}")
        self.episodes: tp.List[Episode] = []
        self.headers: tp.Dict = {}
        _old_eps = Database().get_episodes(self._url)
        _feed = self._get_feed(protected)
        self._name = html.unescape(_feed.feed.get("title", default=self._url))
        try:
            self._image = _feed.feed.image.href
        except (KeyError, AttributeError):
            self._logger.exception(f"No image for {self._url}")
            self._image = None
        self._new_entries = [item for item in _feed.entries if item.id not in _old_eps]
        self._episode_parser()

    def __enter__(self):
        """Context method."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context method."""
        if exc_type is not None:
            self._logger.error(exc_type, exc_val, exc_tb)

    def __repr__(self):
        """`repr` method."""
        return f"{self.__class__.__name__}({self._url}, {self._dl_dir}"

    def __str__(self):
        """`str` method."""
        return f"<Podcast {self._name}>"

    def _get_feed(self, protected: bool) -> fp.FeedParserDict:
        """Get, then parse url; handle keyring interaction,set headers."""
        if protected:
            try:
                credentials = keyring.get_password("podd", self._url)
                self.headers = {"Authorization": "Basic " + credentials}
            except KeyringError:
                self._logger.error(
                    f"Unable to open keyring, failed to update {self._name}"
                )
        resp = get(self._url, headers=self.headers)
        return fp.parse(resp.text)

    def _episode_parser(self) -> None:
        """Create Episodes from FeedParser entries."""
        if self._new_entries:
            self.episodes = [
                Episode(self._dl_dir, entry, self._name, self._url, self.headers)
                for entry in self._new_entries
            ]
            plural = "" if len(self.episodes) == 1 else "s"
            self._logger.debug(
                f"{len(self.episodes)} new episode{plural} of {self._name}"
            )
        else:
            self._logger.debug(f"No episodes for {self._name}")

    @property
    def good_episodes(self):
        """Obtain which episodes were successfully downloaded."""
        one_good = False
        for episode in self.episodes:
            if not episode.error:
                one_good = True
                break
        if one_good:
            return self._name, self._image, [ep for ep in self.episodes if not ep.error]


class Episode:
    """Define `Episode` model.

    Contains data and methods to generate that data, about a single podcast episode
    """

    types = (".mp3", ".m4a", ".aif")

    __slots__ = [
        "_dl_dir",
        "entry",
        "podcast_name",
        "_logger",
        "podcast_url",
        "title",
        "summary",
        "image",
        "url",
        "filename",
        "error",
        "headers",
    ]

    def __init__(
        self,
        directory: str,
        entry: fp.FeedParserDict,
        podcast_name: str,
        podcast_url: str,
        headers,
    ):
        """`init` method.

        :param directory: download directory
        :param entry: single FeedParserDict from fp.parse(url).entries list
        :param podcast_name:
        """
        self.headers = headers
        self._dl_dir = directory
        self.error: bool = False
        self.entry = entry
        self.podcast_name = podcast_name
        self._logger = logger(f"{self.__class__.__name__}")
        self.podcast_url = podcast_url
        self.title = html.unescape(
            self.entry.get("title", "No title available.").replace("/", "-")
        )  # '/' screws up filenames
        self.summary = self.entry.get("summary", "No summary available.")
        self.image = self._image_url()
        self.url = self._audio_file_url()
        self.filename = self._file_parser()

    def __repr__(self):
        """`repr` method."""
        return (
            f"{self.__class__.__name__}({self._dl_dir}, {self.entry}, "
            f"{self.podcast_name}, {self.podcast_url})"
        )

    def __str__(self):
        return f"<Episode {self.title}>"

    def download(self) -> None:
        """Download episode.

        Attempts to download episode
        :return: None
        """
        try:
            resp = get(self.url, stream=True, headers=self.headers)
            if resp.ok:
                with open(self.filename, "wb") as file:
                    for chunk in resp:
                        file.write(chunk)
            self._logger.info(f"Downloaded {self.filename}")
        except FileNotFoundError:
            msg = f"Unable to open file or directory at {self.filename}."
            self._logger.exception(msg)
            self.error = True
            print(msg)
        except (
            ConnectionRefusedError,
            HTTPError,
            URLError,
            CertificateError,
            ConnectionError,
        ) as error:
            msg = f"Error {error} URL: {self.url} Filename: {self.filename}"
            self._logger.exception(msg)
            self.error = True
            print(msg)

    def tag(self) -> None:
        """Tag downloaded file with metadata.

        Uses mutagen's File class to try to discover what type of audio file
        is being tagged, then uses either mp3 or mp4 tagger on file, if type
        is either mp3 or mp4.  Otherwise, passes
        :return: None
        """
        if self.error:
            return
        try:
            filetype = mutagen.File(self.filename).pprint()
            if "mp3" in filetype:
                self._mp3_tagger()
            elif "mp4" in filetype:
                self._mp4_tagger()
            else:
                self._logger.warning(
                    f"Unable to determine filetype for {self.filename}, cannot tag"
                )
        except (AttributeError, mutagen.MutagenError):
            self._logger.exception(f"Unable to tag {self.filename}")

    def _image_url(self):
        """Parse image url.

        Doing the error parsing here instead of just in a pair of nested .get() calls
        because this is both clearer and it doesn't matter at which level the
        dictionary lookup fails, any lookup failure means that there isn't an image url.
        :return: URL to episode image if it exists, else None.
        """
        try:
            image = self.entry.image.href
        except AttributeError:
            image = None
            self._logger.info(
                f"No image found for {self.podcast_name}" f" episode {self.title})"
            )
        return image

    def _audio_file_url(self) -> str:
        """Parse audio file url.

        :return: link for episode's audio file URL.
        """
        url = None
        for link in self.entry.links:
            if "audio/" in link.type:
                url = link.href
                break
        return url

    def _file_parser(self) -> path:
        """Create absolute filename.

        :return: str, ex: path/to/podcast/directory/episode.m4a
        Defaults to .mp3 as that's the most common filetype.

        Recently (As of 04/10/19), of the iTunes top 100 podcasts, 11784/11797, or
        around 99.89%, of all episodes were mp3s.
        """
        for ext in self.types:
            if ext in self.url.lower():  # Edge case where extension is capitalized
                return path.join(self._dl_dir, "".join([self.title, ext]))
        self._logger.warning(
            f"Unable to determine extension for {self.url}, defaulting to `.mp3`"
        )
        return path.join(self._dl_dir, "".join([self.title, ".mp3"]))

    def _mp3_tagger(self) -> None:
        """Tag mp3 files.

        Uses mutagen to write tags to mp3 file
        :return: None
        """
        try:
            tag = EasyID3(self.filename)
        except ID3NoHeaderError:
            self._logger.info(f"Adding header to {self.filename}")
            tag = mutagen.File(self.filename, easy=True)
            tag.add_tags()

        ep_num = self._episode_num_parser()
        tag["title"] = self.title
        tag["artist"] = self.podcast_name
        tag["album"] = self.podcast_name
        tag["albumartist"] = self.podcast_name
        tag["genre"] = "Podcast"
        if ep_num:
            tag["tracknumber"] = ep_num
        tag.save(self.filename)
        self._logger.info(f"Tagged {self.filename}")

    def _mp4_tagger(self) -> None:
        """Tag mp4 files.

        Per https://mutagen.readthedocs.io/en/latest/api/mp4.html#mutagen.mp4.MP4Tags,
        track numbers are tuples of ints, first being track number, the second is
        the total number of tracks, e.g.,  Album X has 10 tracks, we want to tag the
        3rd track, so `tag['trkn'] = (3, 10)`, the weird syntax is because mutagen
        supports multiple keys per track number.  I wish the documentation was
        clearer.  One was chosen as the track count as I had to choose some number:
        leaving it blank isn't an option.

        :return: None
        """
        ep_num = self._episode_num_parser()
        tag = MP4(self.filename).tags
        tag["\xa9nam"] = self.title
        tag["\xa9ART"] = self.podcast_name  # Artist
        tag["\xa9alb"] = self.podcast_name  # Album
        tag["aART"] = self.podcast_name  # Album artist
        tag["\xa9gen"] = "Podcast"  # Genre
        if ep_num:
            tag["trkn"] = ((ep_num, 1),)  # I know this is weird: see docstring
        tag.save(self.filename)
        self._logger.info(f"Tagged {self.filename}")

    def _episode_num_parser(self) -> str or None:
        """Attempt to parse episode number from title."""
        for pattern in PATTERNS:
            match = pattern.search(self.title)
            if match:
                return match.groups()[0]

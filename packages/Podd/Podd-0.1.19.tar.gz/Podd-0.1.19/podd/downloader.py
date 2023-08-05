"""Contain update and download functions."""

import asyncio
from multiprocessing.dummy import Pool as ThreadPool
from typing import List

from podd.database import Database
from podd.message import Message
from podd.podcast import Episode, Podcast


def downloader() -> None:
    """Download all new episodes.

    Refreshes subscriptions, downloads new episodes, sends email messages.
    :return: None.
    """
    with Database() as _db:
        _, send_notifications, _ = _db.get_options()
        if send_notifications:
            sender, password, recipient = _db.get_credentials()
            if not password:
                send_notifications = False
                print("Unable to fetch password from keyring, notifications disabled.")
        podcasts, eps_to_download = threaded_update(_db.get_podcasts())
    if podcasts and eps_to_download:
        threaded_downloader(eps_to_download)
        if send_notifications:
            message_packet = [
                p.good_episodes for p in podcasts if p.good_episodes is not None
            ]
            if message_packet:
                Message(message_packet, sender, password, recipient).send()
    else:
        print("No new episodes")


def threaded_update(subscriptions: list) -> tuple:
    """Create a ThreadPool to get new episodes to download from rss feed.

    :param subscriptions: list of tuples of names, rss feed urls and download
    directories of individual podcasts
    :return: 2-tuple of lists of jinja_packets and a list of episodes to download.
    """

    def update_worker(subscription: tuple) -> Podcast or None:
        """Get update for single podcast.

        Function used by ThreadPool to update RSS feed.
        :param subscription: tuple of name, rss feed url and download directory
        :return:
        """
        # Workaround for jeepney see https://gitlab.com/takluyver/jeepney/issues/6
        asyncio.set_event_loop(asyncio.new_event_loop())
        name, url, dl_dir, protected = subscription
        print(f"{name}...")
        with Podcast(url, dl_dir, protected) as pod:
            if pod.episodes:
                return pod

    podcasts, episodes = [], []
    pool = ThreadPool(3)
    results = pool.map(update_worker, subscriptions)
    pool.close()
    pool.join()
    for podcast in results:
        if podcast:
            podcasts.append(podcast)
            episodes.extend(podcast.episodes)
    return podcasts, episodes


def threaded_downloader(eps_to_download: List[Episode]) -> None:
    """Create thread-pool to download episodes.

    :param eps_to_download: list of Episodes to be downloaded
    :return: None
    """

    def download_worker(episode: Episode) -> Episode:
        """Download and tag episode.

        Function used by ThreadPool.map to download each episode.
        :param: episode Episode obj
        :return: Noned
        """
        print(f"Downloading {episode.podcast_name} - {episode.title}")
        episode.download()
        episode.tag()
        if not episode.error:
            return episode

    if eps_to_download:
        pool = ThreadPool(3)
        results = pool.map(download_worker, eps_to_download)
        pool.close()
        pool.join()
        with Database() as _db:
            for epi in results:
                if epi:
                    _db.add_episode(podcast_url=epi.podcast_url, feed_id=epi.entry.id)

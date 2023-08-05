"""Implement CLI."""

import click

from podd.database import Feed, Options
from podd.downloader import downloader
from podd.settings import Config


@click.command()
@click.option(
    "--catalog",
    is_flag=True,
    default=False,
    help="Download all available episodes, rather than just the newest one.",
)
@click.option(
    "--file",
    is_flag=True,
    default=False,
    help="Specify that the input is a file of RSS feed URLs.",
)
@click.argument("feed")
def add(feed: str, catalog: bool, file: bool):
    """Add podcast subscription using supplied RSS feed URL.

    If the --catalog flag is set, then all available episodes will be downloaded,
    not just the newest episode.  The default behavior causes only the latest
    episode to be downloaded.

    If the --file flag is set, then you can supply a filename as the `feed` argument
    to be able to add multiple podcasts at once.  Simply put each RSS feed URL on its
    own line and Podd will attempt to add each URL.

    """
    if file:
        try:
            with open(feed) as file:
                urls = [l.strip() for l in file if l.strip()]
        except FileNotFoundError:
            return print(f"file `{file}` not found.")
        with Feed() as podcast:
            for url in urls:
                podcast.add(url, newest_only=not catalog)
    else:
        Feed().add(feed, newest_only=not catalog)


@click.command()
@click.argument("directory")
def dir(directory: str):
    """Set download directory.

    Yes, the name overwrites the `dir` builtin, but the command name will be dir.
    Fight me.
    """
    Options().set_directory_option(directory)


@click.command()
def dl():
    """Download all new episodes."""
    downloader()


@click.command()
def email():
    """Setup email notifications."""
    Options().email_notification_setup()


@click.command()
def ls():
    """Print current subscriptions."""
    Feed().print_subscriptions()


@click.command()
def opt():
    """Print currently set options."""
    Options().print_options()


@click.command()
def rm():
    """Interactive subscription deletion menu."""
    Feed().remove()


@click.command()
def v():
    """Print version number."""
    print(Config.version)


@click.group()
def cli_group():
    """Group cli commands"""
    pass


cli_group.add_command(add)
cli_group.add_command(dir)
cli_group.add_command(dl)
cli_group.add_command(email)
cli_group.add_command(ls)
cli_group.add_command(opt)
cli_group.add_command(rm)
cli_group.add_command(v)

"""
Command-line utilities
======================

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
from typing import Optional

import click

# User-contributed libraries
from pyshakealert.message.clients.stomp import Client

from pyshakealert.config import get_app_settings, LogLevels

from pyshakealert.player import CSVPlayer

settings = get_app_settings()


@click.command()
@click.option(
    '-H', '--host',
    default=settings.amq_host,
    help='shakealert host'
)
@click.option(
    '-P', '--port',
    type=int,
    default=settings.amq_stomp_port,
    help='shakealert port'
)
@click.option(
    '-u', '--username',
    default=settings.amq_username,
    help='shakealert AMQ username'
)
@click.option(
    '-p', '--password',
    help='shakealert AMQ password'
)
@click.option(
    '-f', '--file',
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    required=True,
    help='play CSV file'
)
@click.option('--dry-run', is_flag=True)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    host: str,
    port: int,
    username: str,
    password: Optional[str],
    file: str,
    dry_run: bool,
    log_level: Optional[str],
):
    """
    Play a CSV file with ShakeAlert information (uses STOMP)
    """
    settings.amq_host = host
    settings.amq_stomp_port = port
    settings.amq_username = username
    if password is not None:
        settings.amq_password = password
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    # for STOMP user-creds are required
    if settings.amq_username is None or settings.amq_password is None:
        raise ValueError('username and password are required')

    # setup the player
    player = CSVPlayer(file, dry_run=dry_run)

    # set client
    client = Client(
        settings.amq_host,
        username=settings.amq_username,
        password=settings.amq_password,
        ca_certs=settings.amq_ca_certs,
        keyfile=settings.amq_keyfile)

    # play the event on the client
    player.play(client)

    client.disconnect()

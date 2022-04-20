"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
from typing import Optional

import click

# User-contributed libraries
from pyshakealert.message.client import Client

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
    default=settings.amq_port,
    help='shakealert port'
)
@click.option(
    '-u', '--username',
    required=True,
    help='shakealert AMQ username'
)
@click.option(
    '-p', '--password',
    required=True,
    help='shakealert AMQ password'
)
@click.option(
    '-f', '--file',
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    required=True,
    help='play CSV file'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    host: str,
    port: int,
    username: str,
    password: str,
    file: str,
    log_level: Optional[str],
):
    """
    ShakeAlert message sender (simplified stomp utility)

    Send messages on any topic on the ShakeAlert system
    and output the result to stdout
    """
    settings.amq_host = host
    settings.amq_port = port
    settings.amq_username = username
    settings.amq_password = password
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    # setup the player
    player = CSVPlayer(file)

    # set client
    client = Client(settings.amq_host, port=settings.amq_port)
    client.connect(
        username=settings.amq_username,
        password=settings.amq_password)

    # play the event on the client
    player.play(client)

    client.disconnect()

"""
Command-line utilities
======================

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
from typing import Optional

import click

import sys

import logging

# User-contributed libraries
from pyshakealert.message.clients.stomp import Client

from pyshakealert.config import get_app_settings, LogLevels

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
    '-t', '--topic',
    required=True,
    help='shakealert AMQ topic (ex: eew.sys.dm.data)'
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
    help='read content from file (default: stdin)'
)
@click.option(
    '-e', '--expires',
    type=int,
    default=settings.message_expires,
    help='message expiry time in seconds from now'
)
@click.option(
    '-m', '--message-type',
    default='new',
    help='event message type'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    host: str,
    port: int,
    topic: str,
    username: Optional[str],
    password: Optional[str],
    file: Optional[str],
    expires: int,
    message_type: str,
    log_level: Optional[str],
):
    """
    ShakeAlert message sender (uses STOMP)

    Send messages on any topic on the ShakeAlert system.
    """
    settings.amq_host = host
    settings.amq_stomp_port = port
    settings.message_expires = expires
    settings.amq_username = username
    if password is not None:
        settings.amq_password = password

    # for STOMP user-creds are required
    if settings.amq_username is None or settings.amq_password is None:
        raise ValueError('username and password are required')

    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    # Read content to send
    if file is None:
        logging.info('Reading message from stdin')
        body = sys.stdin.read()
    else:
        logging.info(f'Reading message from {file}')
        body = open(file, 'r').read()

    # set signal handlers for stoping listener
    client = Client(
        settings.amq_host,
        port=settings.amq_stomp_port,
        username=settings.amq_username,
        password=settings.amq_password,
        ca_certs=settings.amq_ca_certs,
        keyfile=settings.amq_keyfile)
    client.publish(
        topic=topic,
        body=body,
        message_type=message_type,
    )
    client.disconnect()

"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
from typing import Optional, List

import click

import signal

import logging

import stomp

import time

import traceback

# User-contributed libraries
from pyshakealert.message.client import Client

import pyshakealert.message.event as event

from pyshakealert.actions.mail import Mailer

from pyshakealert.config import get_app_settings, LogLevels

settings = get_app_settings()


class GracefulKiller:
    '''
    Handler for safely terminating the infinite loop programe
    '''
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        logging.info('graceful killer trigger, stop')
        self.kill_now = True


class Listener(stomp.ConnectionListener):
    '''
    ActiveMQ listener to convert and send to NPAS
    '''
    def __init__(self, mailer: Mailer, client: Client):
        self.mailer = mailer
        self.client = client
        self.running = True

    def on_error(self, frame):
        logging.error(f'received an error: {frame}')
        self.running = False
        return super().on_error()

    def on_message(self, frame):
        logging.info(f'received a message: {frame.body}')
        try:
            self.mailer.send(event.from_string(frame.body))
        except Exception:
            logging.error(traceback.format_exc())

    def on_disconnected(self):
        logging.warning('Loss connection')
        self.client.reconnect()


@click.command()
@click.option(
    '-t', '--topic',
    required=True,
    help='shakealert AMQ topic (ex: eew.sys.dm.data)'
)
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
    help='shakealert AMQ username'
)
@click.option(
    '-p', '--password',
    help='shakealert AMQ password'
)
@click.option(
    '-r', '--recipients',
    multiple=True,
    help='recipients for sending email'
)
@click.option(
    '-R', '--recipients-from-file',
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    help='recipients for sending email from file'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    topic: str,
    host: str,
    port: int,
    username: Optional[str],
    password: Optional[str],
    recipients: Optional[List[str]],
    recipients_from_file: Optional[str],
    log_level: Optional[str],
):
    """
    ShakeAlert message sender (simplified stomp utility)

    Send messages on any topic on the ShakeAlert system
    and output the result to stdout
    """
    settings.amq_host = host
    settings.amq_port = port
    if username is not None:
        settings.amq_username = username
    if password is not None:
        settings.amq_password = password
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    emails: List[str] = []
    if recipients_from_file is not None:
        emails = open(recipients_from_file).readlines()
        emails = [email.strip() for email in emails]
        emails = list(filter(len, emails))
    if recipients is not None:
        emails += recipients
    if len(emails) == 0:
        raise IOError('No email recipients found')

    logging.info(f'Registering emails: {emails}')

    client = Client(
        settings.amq_host,
        port=settings.amq_port,
        username=settings.amq_username,
        password=settings.amq_password,
        keepalive=True,
        heartbeats=(4000, 4000))
    # Create the mail client listener
    listener = Listener(
        mailer=Mailer(recipients=emails),
        client=client,
    )
    client.connect()
    client.listen(topic, listener=listener)

    # set signal handlers for stoping listener
    killer = GracefulKiller()
    while not killer.kill_now and listener.running:
        time.sleep(1)

    # terminate the connection cleanly for the ActiceMQ broker
    client.disconnect()

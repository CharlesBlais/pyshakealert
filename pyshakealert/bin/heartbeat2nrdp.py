"""
Command-line utilities
======================

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
from typing import Optional

import click

import signal

import logging

import time

# User-contributed libraries
from pyshakealert.message.clients.mqtt import Client

import pyshakealert.message.system_status as system_status

from pyshakealert.nagios import nrdp

from pyshakealert.config import get_app_settings, LogLevels

from pyshakealert.nagios.models import NagiosRange


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


@click.command()
@click.option(
    '-t', '--topic',
    required=True,
    help='shakealert HA AMQ topic (ex: eew.sys.ha.data)'
)
@click.option(
    '-H', '--host',
    default=settings.amq_host,
    help='shakealert host'
)
@click.option(
    '-P', '--port',
    type=int,
    default=settings.amq_mqtt_port,
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
    '--nagios-url',
    default=settings.nagios_url,
    help='Nagios XI host'
)
@click.option(
    '--nagios-token',
    default=settings.nagios_token,
    help='Nagios XI tocken'
)
@click.option(
    '-w', '--warning',
    default=settings.nagios_timestamp_warning,
    help='Warning threshold in seconds for old timestamp'
)
@click.option(
    '-c', '--critical',
    default=settings.nagios_timestamp_critical,
    help='Critical threshold in seconds for old timestamp'
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
    username: str,
    password: Optional[str],
    nagios_url: Optional[str],
    nagios_token: Optional[str],
    warning: str,
    critical: str,
    log_level: Optional[str],
):
    """
    ShakeAlert message sender (simplified stomp utility)

    Send messages on any topic on the ShakeAlert system
    and output the result to stdout
    """
    settings.amq_host = host
    settings.amq_mqtt_port = port
    settings.amq_username = username
    settings.nagios_url = nagios_url
    settings.nagios_token = nagios_token
    settings.nagios_timestamp_warning = warning
    settings.nagios_timestamp_critical = critical
    if password is not None:
        settings.amq_password = password
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    if settings.nagios_token is None or settings.nagios_token is None:
        raise ValueError('Nagios URL and token must be defined')

    def on_message(topic, payload):
        nrdp.submit(
            nrdp=nrdp.to_nrdp(
                hostname=settings.amq_host,
                system_status=system_status.from_string(payload),
                warning=NagiosRange(settings.nagios_timestamp_warning),
                critical=NagiosRange(settings.nagios_timestamp_critical),
            ),
            nagios_url=settings.nagios_url,
            nagios_token=settings.nagios_token,
        )

    client = Client(
        settings.amq_host,
        port=settings.amq_mqtt_port,
        username=settings.amq_username,
        password=settings.amq_password,
        ca_certs=settings.amq_ca_certs,
        keyfile=settings.amq_keyfile,
        reconnect=10)
    client.subscribe(topic, on_message=on_message)

    # set signal handlers for stoping listener
    killer = GracefulKiller()
    while not killer.kill_now:
        time.sleep(1)

    # terminate the connection cleanly for the ActiceMQ broker
    client.disconnect()

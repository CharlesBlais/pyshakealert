"""
Command-line utilities
======================

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
from typing import Optional

import datetime

import click

import sys
import logging
import getpass

# Third-party library
from obspy.clients.fdsn.client import Client
from obspy import UTCDateTime

# User-contributed libraries
import pyshakealert.channels.file
from pyshakealert.config import get_app_settings, LogLevels


settings = get_app_settings()


@click.command()
@click.option(
    '--fdsnws',
    default=settings.fdsnws,
    help='FDSNWS'
)
@click.option(
    '--network',
    default='CN',
    help='network code pattern'
)
@click.option(
    '--station',
    default='*',
    help='station code pattern'
)
@click.option(
    '--station',
    default='*',
    help='station code pattern'
)
@click.option(
    '--location',
    default='*',
    help='location code pattern'
)
@click.option(
    '--channel',
    default='HN?',
    help='channel code pattern'
)
@click.option(
    '--starttime',
    type=click.DateTime(),
    help='only use station within start time'
)
@click.option(
    '--endtime',
    type=click.DateTime(),
    help='only use station within end time'
)
@click.option(
    '--output',
    type=click.Path(file_okay=True, dir_okay=False, exists=False),
    help='only use station within end time'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity')
def main(
    fdsnws: str,
    network: str,
    station: str,
    location: str,
    channel: str,
    starttime: Optional[datetime.datetime],
    endtime: Optional[datetime.datetime],
    output: Optional[str],
    log_level: Optional[str],
):
    """
    Query FDSN-WS to generate channel file

    Note that "pattern" refers to standard FDSNWS
    pattern for station selection.
    """
    settings.fdsnws = fdsnws
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    logging.info(f'Connection to FDSN-WS: {settings.fdsnws}')
    client = Client(settings.fdsnws)

    logging.info(
        f'Getting inventory for {network}.{station}.{location}.{channel}')

    st = UTCDateTime(starttime) if starttime is not None else None
    et = UTCDateTime(endtime) if endtime is not None else None

    inventory = client.get_stations(
        network=network,
        station=station,
        location=location,
        channel=channel,
        level='response',
        starttime=st,
        endtime=et,
    )

    logging.info(f'Inventory found: {inventory}')

    routput = sys.stdout if output is None else output
    user = getpass.getuser()
    pyshakealert.channels.file.write(
        routput, inventory, user=user)  # type: ignore

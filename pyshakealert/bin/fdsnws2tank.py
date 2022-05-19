"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
import datetime
from typing import Optional

import click

import sys

# Third-party libraries
from obspy.core.event import read_events

# User-contributed libraries
from pyshakealert.tankplayer import tankfile
from pyshakealert.config import get_app_settings, LogLevels

# Constants
DEFAULT_PAD_BEFORE = 120  # seconds
DEFAULT_PAD_AFTER = 300  # seconds
DEFAULT_BUFFER_SIZE = 5  # seconds


settings = get_app_settings()


@click.command()
@click.option(
    '--fdsnws',
    help='FDSNWS'
)
@click.option(
    '--eventid',
    help='Event ID to request from the FDSN-WS'
)
@click.option(
    '--quakeml',
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    help='QuakeML information to use to get waveform data \
(overwrite --eventid)'
)
@click.option(
    '--pad-before',
    type=int,
    default=DEFAULT_PAD_BEFORE,
    help='pad before in seconds'
)
@click.option(
    '--pad-after',
    type=int,
    default=DEFAULT_PAD_AFTER,
    help='pad after in seconds'
)
@click.option(
    '--buffer-size',
    type=int,
    default=DEFAULT_BUFFER_SIZE,
    help='split traces in streams by seconds'
)
@click.option(
    '--radius',
    type=float,
    default=DEFAULT_BUFFER_SIZE,
    help='Radius in degrees to take from the event location.  \
If not set, the stations with picks will be selected.'
)
@click.option(
    '--force-starttime',
    type=click.DateTime(),
    help='force starttime to this time'
)
@click.option(
    '--output',
    type=click.Path(file_okay=True, dir_okay=False, exists=False),
    help='only use station within end time'
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help='Verbosity'
)
def main(
    fdsnws: str,
    eventid: Optional[str],
    quakeml: Optional[str],
    pad_before: int,
    pad_after: int,
    buffer_size: int,
    radius: Optional[float],
    force_starttime: Optional[datetime.datetime],
    output: str,
    log_level: Optional[str],
):
    """
    Query FDSN-WS for event information (or quakeml file) and \
extract miniseed information to convert into tank file.
    """
    settings.fdsnws = fdsnws
    if log_level is not None:
        settings.log_level = LogLevels[log_level]
    settings.configure_logging()

    tankgen = tankfile.TankGenerator()

    if quakeml is not None:
        tankcontent = tankgen.from_event(
            read_events(quakeml),
            radius=radius,
            pad_before=pad_before,
            pad_after=pad_after,
            force_starttime=force_starttime)
    elif eventid is not None:
        tankcontent = tankgen.from_eventid(
            eventid,
            radius=radius,
            pad_before=pad_before,
            pad_after=pad_after,
            buffer_size=buffer_size,
            force_starttime=force_starttime)
    else:
        raise IOError('eventid or quakml file must be specified as argument')

    routput = sys.stdout.buffer if output is None else open(output, 'wb')
    routput.write(tankcontent)

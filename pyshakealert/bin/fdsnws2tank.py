"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
import argparse
import sys
import logging

# Third-party libraries
from obspy.core.event import read_events
from dateutil.parser import parse

# User-contributed libraries
from pyshakealert.tankplayer import tankfile
from pyshakealert.config import get_app_settings

# Constants
DEFAULT_PAD_BEFORE = 120  # seconds
DEFAULT_PAD_AFTER = 300  # seconds
DEFAULT_BUFFER_SIZE = 5  # seconds


def fdsnws2tank():
    """
    Call the FDSN-WS, extract the event and waveform information
    """
    settings = get_app_settings()

    parser = argparse.ArgumentParser(
        description='Query FDSN-WS for event information (or quakeml file) and \
extract miniseed information.')
    parser.add_argument(
        '--fdsnws',
        default=settings.fdsnws,
        help=f'FDSNWS (default: {settings.fdsnws})')
    parser.add_argument(
        '--eventid',
        default=None,
        help='Event ID to request from the FDSN-WS')
    parser.add_argument(
        '--quakeml',
        default=None,
        help='QuakeML information to use to get waveform data \
(overwrite --eventid)')
    parser.add_argument(
        '--pad-before',
        default=DEFAULT_PAD_BEFORE,
        type=float,
        help=f'Pad before in seconds (default: {DEFAULT_PAD_BEFORE})')
    parser.add_argument(
        '--pad-after',
        default=DEFAULT_PAD_AFTER,
        type=float,
        help=f'Pad after in seconds (default: {DEFAULT_PAD_AFTER})')
    parser.add_argument(
        '--buffer-size',
        default=DEFAULT_BUFFER_SIZE,
        type=float,
        help=f'Split traces in streams by seconds \
(default: {DEFAULT_BUFFER_SIZE})')
    parser.add_argument(
        '--radius',
        default=None,
        help='Radius in degrees to take from the event location.  \
If not set, the stations with picks will be selected.')
    parser.add_argument(
        '--force-starttime',
        default=None,
        help='Force starttime to this time')
    parser.add_argument(
        '--output',
        default=sys.stdout.buffer,
        help='Output file (default: stdout)')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbosity')
    args = parser.parse_args()

    # Set logging level
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(funcName)s:\
            %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO if args.verbose else logging.WARNING)

    if args.eventid is None and args.quakeml is None:
        raise IOError('eventid or quakml file must be specified as argument')

    tankgen = tankfile.TankGenerator(args.fdsnws, application=args.ms2tank)

    force_starttime = None if args.force_starttime is None \
        else parse(args.force_starttime)

    if args.quakeml is not None:
        tankcontent = tankgen.from_event(
            read_events(args.quakeml),
            radius=args.radius,
            pad_before=args.pad_before,
            pad_after=args.pad_after,
            force_starttime=force_starttime)
    else:
        tankcontent = tankgen.from_eventid(
            args.eventid,
            radius=args.radius,
            pad_before=args.pad_before,
            pad_after=args.pad_after,
            buffer_size=args.buffer_size,
            force_starttime=force_starttime)

    logging.info(f'Writting results to {args.output}')
    resource = open(args.output, 'wb') \
        if isinstance(args.output, str) else args.output
    resource.write(tankcontent)

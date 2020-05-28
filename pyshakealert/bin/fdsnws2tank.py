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

# User-contributed libraries
from pyshakealert.tankplayer import tankfile

# Constants
DEFAULT_FDSNWS = 'http://sc3-stage.seismo.nrcan.gc.ca'
DEFAULT_PAD_BEFORE = 60  # seconds
DEFAULT_PAD_AFTER = 600  # seconds
DEFAULT_MS2TANK = '/app/eewdata/ew/bin/ms2tank'


def fdsnws2tank():
    """
    Call the FDSN-WS, extract the event and waveform information
    """
    parser = argparse.ArgumentParser(
        description='Query FDSN-WS for event information (or quakeml file) and \
extract miniseed information.')
    parser.add_argument(
        '--fdsnws',
        default=DEFAULT_FDSNWS,
        help=f'FDSNWS (default: {DEFAULT_FDSNWS})')
    parser.add_argument(
        '--ms2tank',
        default=DEFAULT_MS2TANK,
        help=f'ms2tank application (default: {DEFAULT_MS2TANK})')
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
        help=f'Pad before in seconds (default: {DEFAULT_PAD_BEFORE})')
    parser.add_argument(
        '--pad-after',
        default=DEFAULT_PAD_AFTER,
        help=f'Pad after in seconds (default: {DEFAULT_PAD_AFTER})')
    parser.add_argument(
        '--output',
        default=sys.stdout,
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

    if args.quakeml is not None:
        tankcontent = tankgen.from_event(
            read_events(args.quakeml),
            pad_before=args.pad_before,
            pad_after=args.pad_after)
    else:
        tankcontent = tankgen.from_eventid(
            args.eventid,
            pad_before=args.pad_before,
            pad_after=args.pad_after)

    logging.info(f'Writting results to {args.output}')
    resource = open(args.output, 'wb') \
        if isinstance(args.output, str) else args.output
    resource.write(tankcontent)

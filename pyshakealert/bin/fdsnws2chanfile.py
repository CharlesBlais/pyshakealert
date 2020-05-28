"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
import argparse
import sys
import logging
import getpass

# Third-party library
from obspy.clients.fdsn.client import Client
from obspy import UTCDateTime

# User-contributed libraries
import pyshakealert.channels.file

# Constants
DEFAULT_FDSNWS = 'http://fdsn.seismo.nrcan.gc.ca'
USER = getpass.getuser()


def fdsnws2chanfile():
    """
    Call the FDSN-WS, extract the channel information
    and creates the relevant chanfile
    """
    parser = argparse.ArgumentParser(
        description='Query FDSN-WS to generate channel file')
    parser.add_argument(
        '--fdsnws',
        default=DEFAULT_FDSNWS,
        help='FDSNWS (default: %s)' % DEFAULT_FDSNWS)
    parser.add_argument(
        '--network',
        default='CN',
        help='Network code (default: CN)')
    parser.add_argument(
        '--station',
        default='*',
        help='Station code (default: *)')
    parser.add_argument(
        '--location',
        default='*',
        help='Location code (default: *)')
    parser.add_argument(
        '--channel',
        default='HN?',
        help='Channel code (default: HN?)')
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

    logging.info(f'Connection to FDSN-WS: {args.fdsnws}')
    client = Client(args.fdsnws)

    logging.info(
        f'Getting inventory for {args.network}.{args.station}\
.{args.location}.{args.channel}')

    inventory = client.get_stations(
        network=args.network,
        station=args.station,
        location=args.location,
        channel=args.channel, level='response',
        starttime=UTCDateTime())

    logging.info(f'Inventory found: {inventory}')
    logging.info(f'Writing to {args.output}')
    pyshakealert.channels.file.write(args.output, inventory, user=USER)

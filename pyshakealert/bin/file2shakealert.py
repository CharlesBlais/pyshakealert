"""
Command-line utilities
======================

..  codeauthor:: Charles Blais
"""
import argparse
import sys
import logging
import datetime

# User-contributed libraries
from pyshakealert.message.client import Client

# Constants
DEFAULT_SHAKEALERT_HOST = 'localhost'
DEFAULT_SHAKEALERT_PORT = 61613
SHAKEALERT_STOMP_PORTS = [61613, 62613, 63613]


def file2shakealert():
    """
    Send messages on any topic on the ShakeAlert system
    and output the result to stdout
    """
    parser = argparse.ArgumentParser(
        description='ShakeAlert message sender (simplified stomp utility)')
    parser.add_argument(
        '-H', '--host',
        default=DEFAULT_SHAKEALERT_HOST,
        help='ShakeAlert host (default: %s)' % DEFAULT_SHAKEALERT_HOST)
    parser.add_argument(
        '-P', '--port',
        default=DEFAULT_SHAKEALERT_PORT,
        choices=SHAKEALERT_STOMP_PORTS,
        type=int,
        help='ActiveMQ stomp port (default: %d)' % DEFAULT_SHAKEALERT_PORT)
    parser.add_argument(
        '-t', '--topic',
        default='eew.sys.dm.data',
        help='ShakeAlert topic (default: eew.sys.dm.data)')
    parser.add_argument(
        '-u', '--username',
        required=True,
        help='Username for connection')
    parser.add_argument(
        '-p', '--password',
        default='eew.sys.dm.data',
        help='Password for connection')
    parser.add_argument(
        '-f', '--file',
        help='Read content from file (default: stdin)')
    parser.add_argument(
        '-e', '--expires',
        default=60,
        type=int,
        help='Message expiry time in seconds from now (default: 60)')
    parser.add_argument(
        '-m', '--message-type',
        default='new',
        help='Message type (default: new)')
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
        level=logging.DEBUG if args.verbose else logging.WARNING)

    # Read content to send
    if args.file is None:
        logging.info('Reading message from stdin')
        body = sys.stdin.read()
    else:
        logging.info(f'Reading message from {args.file}')
        body = open(args.file, 'r').read()

    # set signal handlers for stoping listener
    client = Client(args.host, port=args.port)
    client.connect(username=args.username, password=args.password)
    client.send(
        topic=args.topic,
        body=body,
        expires=datetime.timedelta(seconds=args.expires),
        message_type=args.message_type
    )

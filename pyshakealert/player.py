'''
..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
'''
import logging

import time

import datetime

import csv

from typing import List

from pydantic import BaseModel

from pathlib import Path

from pyshakealert.message.clients.stomp import Client

from pyshakealert.message.event import from_file, to_string


class PlayItem(BaseModel):
    send_at: float
    delay: float
    topic: str
    message_type: str
    filename: str


class CSVPlayer:
    '''
    Parse the content of the CSV file to determine
    the timeline of information to play, its topic, and the file content.

    We also validate that the file exists.
    '''
    def __init__(self, csvfile: str, dry_run: bool = False):
        '''
        Constructor

        :param str csvfile: CSV file to parse
        '''
        self.playlist: List[PlayItem] = CSVPlayer._parse(csvfile)
        self.dry_run = dry_run

    @staticmethod
    def _parse(csvfile: str) -> List[PlayItem]:
        '''
        Parse the CSV file into the structure

        :param str csvfile: CSV file to parse

        :rtype: [dict]
        :returns: return list of play items
        '''
        logging.debug(f'Reading content of {csvfile}')
        result: List[PlayItem] = []
        with open(csvfile) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                logging.debug(f'parsing {row}')
                item = PlayItem(**row)

                # The filename is based on the location of the csv file
                item.filename = str(
                    Path(csvfile).parent.joinpath(item.filename))

                if not Path(item.filename).exists():
                    raise ValueError(f'{item.filename} does not exist')
                result.append(item)
        return sorted(result, key=lambda x: x.send_at, reverse=False)

    def play(self, client: Client):
        '''
        Play the content of the CSV file to the client that has already
        initiated a connection.

        ..  note:: the following assumes the client is already connected

        :type client: :class:`pyshakealert.message.client.Client`
        :param client: mesage broker client
        '''
        now = time.time()
        for item in self.playlist:
            delta = time.time() - (now + item.send_at)
            if delta > 0:
                logging.info(f'Waiting {delta} seconds')
                time.sleep(delta)
            logging.info(f'Sending content of {item.filename} to {item.topic}')
            event = from_file(item.filename)

            # alter message format
            event.timestamp = datetime.datetime.utcnow().isoformat()
            event.core_info.orig_time.value = (
                datetime.datetime.utcnow() -
                datetime.timedelta(seconds=item.delay)
            ).isoformat()
            logging.debug(f'  timestamp: {event.timestamp}')
            logging.debug(f'  origin: {event.core_info.orig_time.value}')

            if not self.dry_run:
                logging.info('Sending...')
                client.publish(
                    topic=item.topic,
                    body=to_string(event),
                    message_type=item.message_type,
                )
            else:
                logging.info('Quiet mode enabled')

'''
..  codeauthor:: Charles Blais
'''
import logging

import time

import csv

from typing import List

from pydantic import BaseModel

from pathlib import Path

from pyshakealert.message.client import Client


class PlayItem(BaseModel):
    offset: float
    topic: str
    message_type: str
    filename: str


class CSVPlayer:
    '''
    Parse the content of the CSV file to determine
    the timeline of information to play, its topic, and the file content.

    We also validate that the file exists.
    '''
    def __init__(self, csvfile: str):
        self.playlist: List[PlayItem] = self._parse(csvfile)

    def _parse(self, csvfile: str) -> List[PlayItem]:
        '''
        Parse the CSV file into the structure
        '''
        logging.debug(f'Reading content of {csvfile}')
        result: List[PlayItem] = []
        with open(csvfile) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                logging.debug(f'parsing {row}')
                item = PlayItem(**row)
                if not Path(item.filename).exists():
                    raise ValueError(f'{item.filename} does not exist')
                result.append(item)
        return sorted(result, key=lambda x: x.offset, reverse=False)

    def play(
        self,
        client: Client,
    ):
        '''
        ..  note:: the following assumes the client is already connected
        '''
        now = time.time()
        for item in self.playlist:
            delta = time.time() - (now + item.offset)
            if delta > 0:
                logging.info(f'Waiting {delta} seconds')
                time.sleep(delta)
            logging.info(f'Sending content of {item.filename} to {item.topic}')
            content = open(item.filename, 'r').read()
            client.send(
                topic=item.topic,
                body=content,
                message_type=item.message_type,
            )
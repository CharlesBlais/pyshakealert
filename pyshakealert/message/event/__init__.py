'''
..  codeauthor:: Charles Blais
'''
import json

import xmltodict

from pyshakealert.message.event.event import Event


def from_string(content: str) -> Event:
    '''
    Parse from string.  String should be an event_message
    '''
    xmldoc = json.loads(json.dumps(xmltodict.parse(content)))
    if 'event_message' not in xmldoc:
        raise ValueError(
            f'Content of XML should be a event_message, received {content}')
    return Event(**xmldoc['event_message'])


def from_file(filename: str) -> Event:
    '''
    Parse content from file which should be an event_message
    '''
    return from_string(open(filename).read())

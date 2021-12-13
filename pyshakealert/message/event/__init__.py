'''
..  codeauthor:: Charles Blais
'''
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .event import Event


def from_string(content: str) -> Event:
    '''
    Parse from string.  String should be an event_message
    '''
    parser = XmlParser()
    return parser.from_string(content, Event)


def from_file(filename: str) -> Event:
    '''
    Parse content from file which should be an event_message
    '''
    parser = XmlParser()
    return parser.parse(filename, Event)


def to_string(event: Event) -> str:
    '''
    Convert an event to string object
    '''
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    return serializer.render(event)

'''
..  codeauthor:: Charles Blais
'''
from xsdata.formats.dataclass.parsers import XmlParser

from xsdata.formats.dataclass.serializers import XmlSerializer

from xsdata.formats.dataclass.serializers.config import SerializerConfig

from typing import Union

from .system_status import SystemStatus

from .component import Component

from .subcomponent import SubComponent


def from_string(content: str) -> SystemStatus:
    '''
    Parse from string.  String should be an system_status
    '''
    parser = XmlParser()
    return parser.from_string(content, SystemStatus)


def from_file(filename: str) -> SystemStatus:
    '''
    Parse content from file which should be an system_status
    '''
    parser = XmlParser()
    return parser.parse(filename, SystemStatus)


def to_string(
    status: Union[SystemStatus, Component, SubComponent],
) -> str:
    '''
    Convert an event to string object
    '''
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    return serializer.render(status)

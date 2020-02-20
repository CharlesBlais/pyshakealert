'''
ShakeAlert Event
================

Object for handling ShakeAlert Event as described
in XML schema under schema/dm_message.xsd directory

..  codeauthor:: Charles Blais
'''
import datetime
import json
from typing import Union, List, Dict, TextIO, Any, SupportsInt

from dateutil.parser import parse
import xmltodict

from pyshakealert.message.event.core import Core
from pyshakealert.message.event.contributor import Contributors
from pyshakealert.message.event.gm import GroundMotion


class Event(dict):
    '''Event message'''
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        # Create the default required objects
        # attributes
        self.version = self.version
        self.origin_system = self.origin_system
        self.message_type = self.message_type
        # elements
        self.core = self.core
        self.contributors = self.contributors

    @property
    def version(self) -> int:
        '''Get version'''
        return self.get('@version', 0)

    @version.setter
    def version(self, value: SupportsInt) -> None:
        '''Set version'''
        self['@version'] = int(value)

    @property
    def origin_system(self) -> str:
        '''Get origin system'''
        return self.get('@origin_system', 'dm')

    @origin_system.setter
    def origin_system(self, value: str) -> None:
        '''Set origin system'''
        self['@origin_system'] = value

    @property
    def message_type(self) -> str:
        '''Get message type'''
        return self.get('@message_type', 'new')

    @message_type.setter
    def message_type(self, value: str) -> None:
        '''Set message type'''
        accepted = ['new', 'update', 'delete', 'follow_up']
        if value not in accepted:
            raise ValueError("Message type can only be %s" % ", ".join(accepted))
        self['@message_type'] = value

    @property
    def category(self) -> str:
        '''Get category'''
        return self.get('@category', 'live')

    @category.setter
    def category(self, value: str) -> None:
        '''Set category'''
        self['@category'] = value

    @property
    def timestamp(self) -> datetime.datetime:
        '''Get timestamp'''
        return parse(self.get('@timestamp', None))

    @timestamp.setter
    def timestamp(self, value: Union[str, datetime.datetime]) -> None:
        '''Set timestamp'''
        convts = parse(value) if isinstance(value, str) else value
        self['@timestamp'] = convts.isoformat()[:19] + "Z"

    @property
    def algorithm(self) -> str:
        '''Get algorithm version'''
        return self.get('@alg_vers', None)

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        '''Set algorithm version'''
        self['@alg_vers'] = value

    @property
    def instance(self) -> str:
        '''Get instance'''
        return self.get('@instance', None)

    @instance.setter
    def instance(self, value: str) -> None:
        '''Set instance'''
        self['@instance'] = value

    @property
    def reference_id(self) -> str:
        '''Get reference id'''
        return self.get('@ref_id', '-')

    @reference_id.setter
    def reference_id(self, value: str) -> None:
        '''Set reference id'''
        self['@ref_id'] = value

    @property
    def reference_source(self) -> str:
        '''Get reference source'''
        return self.get('@ref_src', None)

    @reference_source.setter
    def reference_source(self, value: str) -> None:
        '''Set reference source'''
        self['@ref_src'] = value

    @property
    def core(self) -> Core:
        '''Get core info'''
        return self.get('core_info', Core())

    @core.setter
    def core(self, value: Dict) -> None:
        '''Set core info'''
        self['core_info'] = Core(**value)

    @property
    def contributors(self) -> Contributors:
        '''Get contributors

        In the xmltodict library, the list of contributors is actually
        stored in the contributor sub-object.  That list can also be a
        dictionary and not a list.  If it's a dictionary, we must convert it.

        ..  note::

            We need to keep the same structure, although it may seem confusing, in
            order to simplify the conversation too and form xml format.
        '''
        value = self.get('contributors', {}).get("contributor", Contributors())
        return Contributors(value) if isinstance(value, dict) else value

    @contributors.setter
    def contributors(self, value: Union[Dict, List[Dict]]) -> None:
        '''Set contributors

        See getter function for details on the structur of contributors
        '''
        conv = [value] if isinstance(value, dict) else value
        # Create the contributors dictionary if it does not exist
        self.setdefault('contributors', {})
        self['contributors']['contributor'] = Contributors(*conv)

    @property
    def gm(self) -> GroundMotion:
        '''Get ground motion info'''
        value = self.get('gm_info', GroundMotion())
        # optional field so force convert if requested
        return GroundMotion(**value) if not isinstance(value, GroundMotion) else value

    @gm.setter
    def gm(self, value: Dict) -> None:
        '''Set ground motion info'''
        self['gm_info'] = GroundMotion(**value)

    def write(
        self,
        filename: Union[str, TextIO],
        format: str = 'xml'
    ) -> None:
        '''Write event information to file

        The following only support writting the information to
        XML file.

        :type filename: str or resource
        :param filename: resource to write too
        :param str format: output format
        '''
        if format not in ['xml']:
            raise ValueError("Only xml format is supported")

        resource = open(filename, 'w') if isinstance(filename, str) else filename

        def converter(element: Any) -> str:
            if isinstance(element, datetime.datetime):
                return element.strftime("%Y-%m-%dT%H:%M:%S.%f")[:19] + "Z"
            return str(element)

        resource.write(
            xmltodict.unparse(
                json.loads(json.dumps(
                    {"event_message": self},
                    default=converter
                ), parse_int=str, parse_float=str)
            )
        )

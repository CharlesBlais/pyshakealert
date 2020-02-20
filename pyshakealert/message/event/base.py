'''
..  codeauthor:: Charles Blais
'''
import datetime
from typing import Union, SupportsFloat

from dateutil.parser import parse


class BaseFloatUnits(dict):
    '''
    Base class handler for float elements with units
    '''
    def __init__(self, *args, **kwargs):
        super(BaseFloatUnits, self).__init__(*args, **kwargs)
        # Create the default required objects
        # elements
        self.value = self.value
        self.units = self.units

    @property
    def value(self) -> float:
        '''Get value'''
        return self.get('#text', 0.0)

    @value.setter
    def value(self, value: SupportsFloat) -> None:
        '''Set value'''
        self['#text'] = float(value)

    @property
    def units(self) -> str:
        '''Get units'''
        return self.get('@units', '')

    @units.setter
    def units(self, value: str) -> None:
        '''Set units'''
        self['@units'] = value


class BaseDatetimeUnits(dict):
    '''
    Base class handler for datetime elements with units
    '''
    def __init__(self, *args, **kwargs):
        super(BaseDatetimeUnits, self).__init__(*args, **kwargs)
        # Create the default required objects
        # elements
        self.value = self.value
        self.units = self.units

    @property
    def value(self) -> datetime.datetime:
        '''Get value'''
        return self.get('#text', datetime.datetime.now())

    @value.setter
    def value(self, value: Union[str, datetime.datetime]) -> None:
        '''Set value'''
        self['#text'] = parse(value) if isinstance(value, str) else value

    @property
    def units(self) -> str:
        '''Get units'''
        return self.get('@units', 'UTC')

    @units.setter
    def units(self, value: str) -> None:
        '''Set units'''
        self['@units'] = value

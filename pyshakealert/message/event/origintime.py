'''
..  codeauthor:: Charles Blais
'''
from pyshakealert.message.event.base import BaseFloatUnits, BaseDatetimeUnits


class OriginTimeUncertainty(BaseFloatUnits):
    '''Event message origin time'''
    def __init__(self, *args, **kwargs):
        super(OriginTimeUncertainty, self).__init__(*args, **kwargs)
        self.units = 'sec'


class OriginTime(BaseDatetimeUnits):
    '''Event message origin time'''
    def __init__(self, *args, **kwargs):
        super(OriginTime, self).__init__(*args, **kwargs)
        self.units = 'UTC'

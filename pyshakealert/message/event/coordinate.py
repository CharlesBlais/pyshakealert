'''
..  codeauthor:: Charles Blais
'''
from pyshakealert.message.event.base import BaseFloatUnits


class CoordinateUncertainty(BaseFloatUnits):
    '''Event message coordinate'''
    def __init__(self, *args, **kwargs):
        super(CoordinateUncertainty, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'deg'


class Coordinate(BaseFloatUnits):
    '''Event message coordinate'''
    def __init__(self, *args, **kwargs):
        super(Coordinate, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'deg'

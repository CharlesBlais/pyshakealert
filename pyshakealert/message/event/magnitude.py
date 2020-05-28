"""
..  codeauthor:: Charles Blais
"""
from pyshakealert.message.event.base import BaseFloatUnits


class MagnitudeUncertainty(BaseFloatUnits):
    """Event message magnitude"""
    def __init__(self, *args, **kwargs):
        super(MagnitudeUncertainty, self).__init__(*args, **kwargs)
        self.units = 'Mw'


class Magnitude(BaseFloatUnits):
    """Event message magnitude"""
    def __init__(self, *args, **kwargs):
        super(Magnitude, self).__init__(*args, **kwargs)
        self.units = 'Mw'

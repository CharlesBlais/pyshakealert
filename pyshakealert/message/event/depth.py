"""
..  codeauthor:: Charles Blais
"""
from pyshakealert.message.event.base import BaseFloatUnits


class DepthUncertainty(BaseFloatUnits):
    """Event message depth"""
    def __init__(self, *args, **kwargs):
        super(DepthUncertainty, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'km'


class Depth(BaseFloatUnits):
    """Event message depth"""
    def __init__(self, *args, **kwargs):
        super(Depth, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'km'

"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from .base import BaseFloatUnits


@dataclass
class MagnitudeUncertainty(BaseFloatUnits):
    units: str = field(
        default='Mw',
        metadata=dict(type="Attribute"))


@dataclass
class Magnitude(BaseFloatUnits):
    units: str = field(
        default='Mw',
        metadata=dict(type="Attribute"))

"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from .base import BaseFloatUnits


@dataclass
class CoordinateUncertainty(BaseFloatUnits):
    units: str = field(
        default='deg',
        metadata=dict(type="Attribute"))


@dataclass
class Coordinate(BaseFloatUnits):
    units: str = field(
        default='deg',
        metadata=dict(type="Attribute"))

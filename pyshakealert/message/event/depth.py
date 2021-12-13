"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from .base import BaseFloatUnits


@dataclass
class DepthUncertainty(BaseFloatUnits):
    units: str = field(
        default='km',
        metadata=dict(type="Attribute"))


@dataclass
class Depth(BaseFloatUnits):
    units: str = field(
        default='km',
        metadata=dict(type="Attribute"))

"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from .base import BaseFloatUnits, BaseDatetimeUnits


@dataclass
class OriginTimeUncertainty(BaseFloatUnits):
    units: str = field(
        default='sec',
        metadata=dict(type="Attribute"))


@dataclass
class OriginTime(BaseDatetimeUnits):
    units: str = field(
        default='UTC',
        metadata=dict(type="Attribute"))

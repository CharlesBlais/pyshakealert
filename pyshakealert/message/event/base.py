"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field


@dataclass
class BaseFloatUnits:
    value: float
    units: str = field(
        default='',
        metadata=dict(type="Attribute"))


@dataclass
class BaseDatetimeUnits:
    value: str
    units: str = field(
        default='UTC',
        metadata=dict(type="Attribute"))

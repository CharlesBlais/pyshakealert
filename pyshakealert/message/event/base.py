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
class BaseStringUnits:
    value: str
    units: str = field(
        default='',
        metadata=dict(type="Attribute"))


@dataclass
class BaseMagnitude(BaseFloatUnits):
    units: str = field(default='Mw', metadata=dict(type="Attribute"))


@dataclass
class BaseDegrees(BaseFloatUnits):
    units: str = field(default='deg', metadata=dict(type="Attribute"))


@dataclass
class BaseKilometers(BaseFloatUnits):
    units: str = field(default='km', metadata=dict(type="Attribute"))


@dataclass
class BaseDatetime(BaseStringUnits):
    units: str = field(default='UTC', metadata=dict(type="Attribute"))


@dataclass
class BaseSeconds(BaseFloatUnits):
    units: str = field(default='sec', metadata=dict(type="Attribute"))


@dataclass
class BaseCentimeters(BaseFloatUnits):
    units: str = field(default='cm', metadata=dict(type="Attribute"))


@dataclass
class BaseMeters(BaseFloatUnits):
    units: str = field(default='m', metadata=dict(type="Attribute"))


@dataclass
class BaseCentimetersSeconds(BaseFloatUnits):
    units: str = field(default='cm/s', metadata=dict(type="Attribute"))


@dataclass
class BaseCentimetersSecondsSeconds(BaseFloatUnits):
    units: str = field(default='cm/s/s', metadata=dict(type="Attribute"))


@dataclass
class BaseG(BaseFloatUnits):
    units: str = field(default='g', metadata=dict(type="Attribute"))


@dataclass
class BaseMMI(BaseFloatUnits):
    pass

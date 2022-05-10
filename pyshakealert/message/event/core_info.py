"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional

from .base import BaseMagnitude, \
    BaseDegrees, \
    BaseKilometers, \
    BaseDatetime, \
    BaseSeconds


@dataclass
class CoreInfo:
    mag: BaseMagnitude

    mag_uncer: BaseMagnitude

    lat: BaseDegrees

    lat_uncer: BaseDegrees

    lon: BaseDegrees

    lon_uncer: BaseDegrees

    depth: BaseKilometers

    depth_uncer: BaseKilometers

    orig_time: BaseDatetime

    orig_time_uncer: BaseSeconds

    likelihood: float

    id: str = field(metadata=dict(type="Attribute"))

    num_stations: Optional[int] = field(default=None)

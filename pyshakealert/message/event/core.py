"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from .magnitude import \
    Magnitude, MagnitudeUncertainty
from .coordinate import \
    Coordinate, CoordinateUncertainty
from .depth import \
    Depth, DepthUncertainty
from .origintime import \
    OriginTime, OriginTimeUncertainty


@dataclass
class Core:
    mag: Magnitude

    mag_uncer: MagnitudeUncertainty

    lat: Coordinate

    lat_uncer: CoordinateUncertainty

    lon: Coordinate

    lon_uncer: CoordinateUncertainty

    depth: Depth

    depth_uncer: DepthUncertainty

    orig_time: OriginTime

    orig_time_uncer: OriginTimeUncertainty

    likelihood: float = field(default=0.0)

    num_stations: int = field(default=0)

    id: str = field(
        default='',
        metadata=dict(type="Attribute"))

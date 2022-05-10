"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional, List

from .base import BaseDegrees, BaseKilometers, BaseMeters


@dataclass
class Vertex:
    lat: BaseDegrees

    lon: BaseDegrees

    depth: BaseKilometers


@dataclass
class Vertices:
    vertex: List[Vertex]


@dataclass
class Slip:
    ss: Optional[BaseMeters] = field(default=None)

    ss_uncer: Optional[BaseMeters] = field(default=None)

    ds: Optional[BaseMeters] = field(default=None)

    ds_uncer: Optional[BaseMeters] = field(default=None)


@dataclass
class SegmentInformation:
    vertices: Vertices

    slip: Optional[Slip] = field(default=None)


@dataclass
class UncertaintyInformation:
    lon_trans: Optional[BaseDegrees] = field(default=None)

    lat_trans: Optional[BaseDegrees] = field(default=None)

    total_len: Optional[BaseKilometers] = field(default=None)

    strike: Optional[BaseDegrees] = field(default=None)

    dip: Optional[BaseDegrees] = field(default=None)


@dataclass
class FaultDescription:
    segment: List[SegmentInformation]

    atten_geom: bool = field(metadata=dict(type="Attribute"))

    segment_number: int = field(metadata=dict(type="Attribute"))

    segment_shape: str = field(metadata=dict(type="Attribute"))

    confidence: Optional[float] = field(default=None)

    global_uncertainty: Optional[UncertaintyInformation] = field(default=None)


@dataclass
class FaultInformation:
    finite_fault: FaultDescription

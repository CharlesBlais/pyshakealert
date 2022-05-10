"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional, List

from .base import BaseCentimeters, \
    BaseCentimetersSeconds, \
    BaseCentimetersSecondsSeconds, \
    BaseDatetime, \
    BaseDegrees, \
    BaseKilometers, \
    BaseSeconds


@dataclass
class DisplacementObservationPoint:
    SNCL: str

    value: BaseCentimeters

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class DisplacementObservation:
    obs: List[DisplacementObservationPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class VelocityObservationPoint:
    SNCL: str

    value: BaseCentimetersSeconds

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class VelocityObservation:
    obs: List[VelocityObservationPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class AccelerationObservationPoint:
    SNCL: str

    value: BaseCentimetersSecondsSeconds

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class AccelerationObservation:
    obs: List[AccelerationObservationPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class DisplacementPredictionPoint:
    SNCL: str

    value: BaseCentimeters

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    value_uncer: BaseCentimetersSeconds

    app_rad: BaseKilometers

    time_uncer: BaseSeconds

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class DisplacementPrediction:
    pred: List[DisplacementPredictionPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class VelocityPredictionPoint:
    SNCL: str

    value: BaseCentimetersSeconds

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    value_uncer: BaseCentimetersSeconds

    app_rad: BaseKilometers

    time_uncer: BaseSeconds

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class VelocityPrediction:
    pred: List[VelocityPredictionPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class AccelerationPredictionPoint:
    SNCL: str

    value: BaseCentimetersSecondsSeconds

    lat: BaseDegrees

    lon: BaseDegrees

    time: BaseDatetime

    value_uncer: BaseCentimetersSeconds

    app_rad: BaseKilometers

    time_uncer: BaseSeconds

    orig_sys: Optional[str] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class AccelerationPrediction:
    pred: List[AccelerationPredictionPoint] = field(
        default_factory=list)

    number: Optional[int] = field(
        default=None, metadata=dict(type="Attribute"))


@dataclass
class GroundMotionPoint:
    pgd_obs: Optional[DisplacementObservation] = field(default=None)

    pgv_obs: Optional[VelocityObservation] = field(default=None)

    pga_obs: Optional[AccelerationObservation] = field(default=None)

    pgd_pred: Optional[DisplacementPrediction] = field(default=None)

    pgv_pred: Optional[VelocityPrediction] = field(default=None)

    pga_pred: Optional[AccelerationPrediction] = field(default=None)

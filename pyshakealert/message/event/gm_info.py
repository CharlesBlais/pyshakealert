"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field
from typing import Optional

from .gmcontour import GroundMotionContourPrediction
from .gmmap import GroundMotionMapPrediction
from .gmpoint import GroundMotionPoint


@dataclass
class GroundMotionInformation:
    gmpoint_obs: Optional[GroundMotionPoint] = field(
        default=None)

    gmpoint_pred: Optional[GroundMotionPoint] = field(
        default=None)

    gmcontour_pred: Optional[GroundMotionContourPrediction] = field(
        default=None)

    gmmap_pred: Optional[GroundMotionMapPrediction] = field(
        default=None)

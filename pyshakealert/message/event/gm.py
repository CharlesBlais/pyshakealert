"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field
from typing import Optional

from .gmcontour import GroundMotionContourPrediction
from .gmmap import GroundMotionMapPrediction


@dataclass
class GroundMotion:
    gmcontour_pred: Optional[GroundMotionContourPrediction] = field(
        default=None)
    gmmap_pred: Optional[GroundMotionMapPrediction] = field(
        default=None)

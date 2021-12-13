"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field
from typing import List

from shapely.geometry import Polygon

import pandas as pd
import geopandas as gpd

from .base import BaseFloatUnits


@dataclass
class GroundMotionPolygon:
    value: str
    number: int = field(metadata=dict(type="Attribute"))

    @property
    def coordinates(self) -> List:
        """Get coordinates of polygon

        For simplicity of converation from and to xmltodict structure,
        we store the information of the polygons as string and convert
        them on request only.
        """
        return [
            [float(coord) for coord in coords.split(',')]
            for coords in self.value.split(' ')
        ]

    def to_shapely(self):
        """Convert object to shapely

        Convert the list of coordinates to a shapely Polygon object.
        For faster processing, we only load the shapely library if its
        request.  We don't check that the return response is a Shapely
        object for simplicity.

        :rtype: :class:`shapely.geometry.Polygon`
        """
        coords = self.coordinates
        if not coords:
            raise ValueError('Can not convert an empty contour to shapely, \
possibly the event does not contain contour information')
        return Polygon([coord[::-1] for coord in self.coordinates])


@dataclass
class GroundMotionMMI(BaseFloatUnits):
    """Event message MMI"""


@dataclass
class GroundMotionPGA(BaseFloatUnits):
    units: str = field(
        default='cm/s/s',
        metadata=dict(type="Attribute"))


@dataclass
class GroundMotionPGV(BaseFloatUnits):
    units: str = field(
        default='cm/s',
        metadata=dict(type="Attribute"))


@dataclass
class GroundMotionContour:
    MMI: GroundMotionMMI
    PGA: GroundMotionPGA
    PGV: GroundMotionPGV
    polygon: GroundMotionPolygon


@dataclass
class GroundMotionContourPrediction:
    number: int = field(
        default=0,
        metadata=dict(type="Attribute"))
    contour: List[GroundMotionContour] = field(
        default_factory=list)

    def to_dataframe(self):
        """Convert the list of contours to dataframe

        The index of the dataframe is the Polygon shape of the contour.

        ..  note::

            The geopandas library is only loaded on request to increase
            performance of the library.

        :rtype: :class:`geopandas.GeoDataFrame`
        """
        return gpd.GeoDataFrame(pd.DataFrame({
            'MMI': [contour.MMI.value for contour in self.contour],
            'PGA': [contour.PGA.value for contour in self.contour],
            'PGV': [contour.PGV.value for contour in self.contour],
        }), geometry=[
            contour.polygon.to_shapely() for contour in self.contour
        ])

"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field
from typing import List

import pandas as pd
import geopandas as gpd


@dataclass
class GroundMotionGridField:
    index: int = field(
        metadata=dict(type="Attribute"))
    name: str = field(
        metadata=dict(type="Attribute"))
    units: str = field(
        default='',
        metadata=dict(type="Attribute"))


@dataclass
class GroundMotionMapPrediction:
    number: int = field(
        default=0,
        metadata=dict(type="Attribute"))
    grid_field: List[GroundMotionGridField] = field(
        default_factory=list)
    grid_data: str = field(
        default='')

    @property
    def grid(self) -> List[List[float]]:
        """Get values of the grid

        For simplicity of converation from and to xmltodict structure,
        we store the information of the polygons as string and convert
        them on request only.
        """
        content: str = self.grid_data
        return [
            [float(coord) for coord in coords.split(" ")]
            for coords in content.strip().split("\n")
        ]

    def to_dataframe(self):
        """Convert the grid to dataframe

        The index of the dataframe is the Point shape in the grid.

        ..  note::

            The geopandas library is only loaded on request to increase
            performance of the library.

        :rtype: :class:`geopandas.GeoDataFrame`
        """
        # create a sorted list of fields
        columns = {}
        for grid_field in self.grid_field:
            columns[grid_field.index] = grid_field.name

        # Create the basic pandas dataframe and convert
        # the LAT and LON columns to geometry points
        df = pd.DataFrame(self.grid, columns=[
            columns[i] for i in sorted(columns)])

        return gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df.LON, df.LAT)
        )

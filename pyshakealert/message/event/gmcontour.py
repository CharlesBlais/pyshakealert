"""
..  codeauthor:: Charles Blais
"""
from typing import Union, List
from pyshakealert.message.event.base import BaseFloatUnits


class GroundMotionPolygon(dict):
    """Event message polygon contour"""
    def __init__(self, *args, **kwargs):
        super(GroundMotionPolygon, self).__init__(*args, **kwargs)

    @property
    def coordinates(self) -> List:
        """Get coordinates of polygon

        For simplicity of converation from and to xmltodict structure,
        we store the information of the polygons as string and convert
        them on request only.
        """
        content: str = self.get('#text', '')
        if not content:
            return []
        return [
            [float(coord) for coord in coords.split(',')]
            for coords in content.split(' ')
        ]

    @coordinates.setter
    def coordinates(self, value: Union[str, List]) -> None:
        """Set coordinates of polygon"""
        if isinstance(value, list):
            self['#text'] = ' '.join([','.join(sublist) for sublist in value])
        else:
            self['#text'] = value
        self['@number'] = self['#text'].count(',')

    def to_shapely(self):
        """Convert object to shapely

        Convert the list of coordinates to a shapely Polygon object.
        For faster processing, we only load the shapely library if its
        request.  We don't check that the return response is a Shapely
        object for simplicity.

        :rtype: :class:`shapely.geometry.Polygon`
        """
        from shapely.geometry import Polygon
        coords = self.coordinates
        if not coords:
            raise ValueError('Can not convert an empty contour to shapely, \
possibly the event does not contain contour information')
        return Polygon([coord[::-1] for coord in self.coordinates])


class GroundMotionMMI(BaseFloatUnits):
    """Event message MMI"""
    def __init__(self, *args, **kwargs):
        super(GroundMotionMMI, self).__init__(*args, **kwargs)


class GroundMotionPGA(BaseFloatUnits):
    """Event message PGA"""
    def __init__(self, *args, **kwargs):
        super(GroundMotionPGA, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'cm/s/s'


class GroundMotionPGV(BaseFloatUnits):
    """Event message PGV"""
    def __init__(self, *args, **kwargs):
        super(GroundMotionPGV, self).__init__(*args, **kwargs)
        if not self.units:
            self.units = 'cm/s'


class GroundMotionContour(dict):
    """GM contour information as described in
    gmcontour_information of schema"""
    def __init__(self, *args, **kwargs):
        super(GroundMotionContour, self).__init__(*args, **kwargs)
        # Create the default required objects
        # elements
        self.mmi = self.mmi
        self.pga = self.pga
        self.pgv = self.pgv
        self.polygon = self.polygon

    @property
    def mmi(self) -> GroundMotionMMI:
        """Get mmi"""
        return self.get('MMI', GroundMotionMMI())

    @mmi.setter
    def mmi(self, value: GroundMotionMMI) -> None:
        """Set mmi"""
        self['MMI'] = GroundMotionMMI(**value)

    @property
    def pga(self) -> GroundMotionPGA:
        """Get pga"""
        return self.get('PGA', GroundMotionPGA())

    @pga.setter
    def pga(self, value: GroundMotionPGA) -> None:
        """Set pga"""
        self['PGA'] = GroundMotionPGA(**value)

    @property
    def pgv(self) -> GroundMotionPGV:
        """Get pgv"""
        return self.get('PGV', GroundMotionPGV())

    @pgv.setter
    def pgv(self, value: GroundMotionPGV) -> None:
        """Set pgv"""
        self['PGV'] = GroundMotionPGV(**value)

    @property
    def polygon(self) -> GroundMotionPolygon:
        """Get polygon"""
        return self.get('polygon', GroundMotionPolygon())

    @polygon.setter
    def polygon(self, value: GroundMotionPolygon) -> None:
        """Set polygon"""
        self['polygon'] = GroundMotionPolygon(**value)


class GroundMotionContours(list):
    """GM contour information as described in
    gmcontour_information of schema"""
    def __init__(self, *args, **kwargs):
        # Convert all args to contributor object
        contours = [GroundMotionContour(**arg) for arg in args]
        if not contours:
            contours = [GroundMotionContour()]
        super(GroundMotionContours, self).__init__(contours, **kwargs)

    def to_dataframe(self):
        """Convert the list of contours to dataframe

        The index of the dataframe is the Polygon shape of the contour.

        ..  note::

            The geopandas library is only loaded on request to increase
            performance of the library.

        :rtype: :class:`geopandas.GeoDataFrame`
        """
        import pandas as pd
        import geopandas

        return geopandas.GeoDataFrame(pd.DataFrame({
            'MMI': [contour.mmi.value for contour in self],
            'PGA': [contour.pga.value for contour in self],
            'PGV': [contour.pgv.value for contour in self],
        }), geometry=[contour.polygon.to_shapely() for contour in self])

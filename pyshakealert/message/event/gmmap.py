'''
..  codeauthor:: Charles Blais
'''
from typing import Union, List, SupportsInt


class GroundMotionMapField(dict):
    '''Grid field as described in gmmap_information of schema'''
    @property
    def index(self) -> int:
        '''Get the index of the data on the map (starts at 1)'''
        return int(self.get('@index', 0))

    @index.setter
    def index(self, value: SupportsInt) -> None:
        '''Set the index of the data in the map'''
        self['@index'] = int(value)

    @property
    def units(self) -> str:
        '''Get the units of the data on the map'''
        return self.get('@units', '')

    @units.setter
    def units(self, value: str) -> None:
        '''Set the units of the data in the map'''
        self['@units'] = value

    @property
    def name(self) -> str:
        '''Get the name of the data on the map'''
        return self.get('@name', '')

    @name.setter
    def name(self, value: str) -> None:
        '''Set the name of the data in the map'''
        allowed = ['LAT', 'LON', 'PGA', 'PGV', 'MMI']
        if value not in allowed:
            raise ValueError(
                "Unsupporte GM map field of %s, must be %s" % (value, ",".join(allowed)))
        self['@name'] = value


class GroundMotionMapFields(list):
    '''Grid fields list as described in gmmap_information of schema'''
    def __init__(self, *args, **kwargs):
        # Convert all args to contributor object
        fields = [GroundMotionMapField(**arg) for arg in args]
        if not fields:
            fields = [GroundMotionMapField()]
        super(GroundMotionMapFields, self).__init__(fields, **kwargs)


class GroundMotionMap(dict):
    '''GM map information as described in gmmap_information of schema'''
    def __init__(self, *args, **kwargs):
        super(GroundMotionMap, self).__init__(*args, **kwargs)
        self.fields = self.fields

    @property
    def fields(self) -> GroundMotionMapFields:
        '''Get grid fields'''
        value = self.get('grid_field', GroundMotionMapFields())
        # optional field so force convert if requested
        return GroundMotionMapFields(*value) \
            if not isinstance(value, GroundMotionMapFields) \
            else value

    @fields.setter
    def fields(self, value: List) -> None:
        '''Set grid fields'''
        self["grid_field"] = GroundMotionMapFields(*value)

    @property
    def grid(self) -> List:
        '''Get values of the grid

        For simplicity of converation from and to xmltodict structure,
        we store the information of the polygons as string and convert
        them on request only.
        '''
        content: str = self.get('grid_data', '')
        return [[float(coord) for coord in coords.split(" ")] for coords in content.split("\n")]

    @grid.setter
    def grid(self, value: Union[str, List]) -> None:
        '''Set value of the grid'''
        if isinstance(value, list):
            self['#text'] = "\n".join([" ".join(sublist) for sublist in value])
        else:
            self['#text'] = value
        self['@number'] = self['#text'].count(",")

    def to_dataframe(self):
        '''Convert the grid to dataframe

        The index of the dataframe is the Point shape in the grid.

        ..  note::

            The geopandas library is only loaded on request to increase performance
            of the library.

        :rtype: :class:`geopandas.GeoDataFrame`
        '''
        import pandas as pd
        import geopandas

        # create a sorted list of fields
        columns = {}
        for field in self.fields:
            columns[field.index] = field.name

        # Create the basic pandas dataframe and convert
        # the LAT and LON columns to geometry points
        df = pd.DataFrame(self.grid, columns=[columns[i] for i in sorted(columns)])

        return geopandas.GeoDataFrame(
            df,
            geometry=geopandas.points_from_xy(df.LON, df.LAT)
        )

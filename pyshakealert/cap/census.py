'''
Census locations
================

Library for handling census geolocation

..  codeauthor:: Charles Blais
'''
import geopandas


class InvalidCensus(Exception):
    '''Invalid census shapefile'''


class Census(object):
    '''Census information

    Handle census information located in geolocation file.  Census files
    can be found under the "shapefiles" location.  Information sent
    to the census program should be in a compressed zip format.

    All coordinates will be sent in WGS84 format so we convert if not in
    this format.

    :param str censusfile: census file
    :param {str, str} columns: rename columns from to to column (dictionary)
    '''
    def __init__(self, censusfile) -> None:
        self.gdf = geopandas.read_file("zip://%s" % censusfile)
        if str(self.gdf.crs) != "epsg:4326":
            self.gdf = self.gdf.to_crs("epsg:4326")

    def get_census_divisions(self, shape):
        '''
        Determine all census information that intersects the shape
        information (shapely object)
        '''
        return self.gdf[self.gdf.intersects(shape)]

    def merge_by_division_id(self, census):
        '''
        Join inplace the content of the other census information by division
        ID.  To simplify merging, we rename any non-english division ID column
        to english version

        The following is assuming the CDUID and relevant geometry are the same
        '''
        columns = {'DRIDU': 'CDUID'}
        # rename local copy if required
        self.gdf.rename(columns=columns, inplace=True)
        census.gdf.rename(columns=columns, inplace=True)
        census.gdf.drop(columns='geometry', inplace=True)
        self.gdf = self.gdf.merge(census.gdf, on='CDUID')
        return self

    def __repr__(self) -> str:
        '''
        Return representation of object
        '''
        return str(self.gdf)

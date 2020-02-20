'''
..  codeauthor:: Charles Blais
'''

import geopandas
from shapely.geometry import box

from pyshakealert.cap.census import Census


def test_shapefile():
    '''Test shapefile

    Test reading the content of a shapefile and convert it to geopandas
    information
    '''
    census = Census("pyshakealert/files/shapefiles/lcd_000a16a_e.zip")
    subset = census.get_census_divisions(box(-75, 44, -78, 47))
    assert not subset.empty


def test_merge():
    '''Test shapefile

    Test reading the content of a shapefile and convert it to geopandas
    information
    '''
    census = Census("pyshakealert/files/shapefiles/lcd_000a16a_e.zip")
    census_fr = Census("pyshakealert/files/shapefiles/ldr_000a16a_f.zip")
    census.merge_by_division_id(census_fr)
    import time
    start_time = time.time()
    census.get_census_divisions(box(-75, 44, -78, 47))
    print(time.time() - start_time)
    assert False
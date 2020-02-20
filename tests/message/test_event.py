'''
..  codeauthor:: Charles Blais
'''
import datetime
import io

import pyshakealert.message.event as event


def test_event():
    '''
    Test reading event read from file
    '''
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    assert message.category == 'test'
    assert message.origin_system == "dm"
    assert message.message_type == "new"
    assert message.version == 0
    assert message.timestamp.replace(tzinfo=None) == datetime.datetime(1868,10,21,15,53,4,0)
    assert message.core.id == "1868_Hayward_M6.8"
    assert message.core.magnitude.value == 6.8
    assert message.core.magnitude.units == "Mw"
    assert message.core.magnitude_uncertainty.value == 1.0
    assert message.core.magnitude_uncertainty.units == "Mw"
    assert message.core.latitude.value == 37.7
    assert message.core.latitude_uncertainty.value == 0.5
    assert message.core.longitude.value == -122.1
    assert message.core.longitude_uncertainty.value == 0.5
    assert message.core.depth.value == 5
    assert message.core.depth_uncertainty.value == 50.0
    assert message.core.origintime.value.replace(tzinfo=None) == datetime.datetime(1868,10,21,15,53,0,0)
    assert message.core.origintime_uncertainty.value == 20.0
    assert message.core.likelihood == 1.0
    assert message.core.stations == 0
    assert message.contributors[0].algorithm_name == "dm"
    assert message.contributors[0].algorithm_version == "-"
    assert message.contributors[0].algorithm_instance == "-"
    assert message.contributors[0].category == "test"
    assert message.contributors[0].event_id == "1868_Hayward_M6.8"
    assert message.contributors[0].version == 0


def test_event_contour():
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    assert message.gm.contours[0].mmi.value == 2.0
    assert message.gm.contours[0].pga.value == 2.848
    assert message.gm.contours[0].pgv.value == 0.2154
    assert message.gm.contours[0].polygon.coordinates[0] == [41.71, -122.1]


def test_event_contour_shapely():
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    shape = message.gm.contours[0].polygon.to_shapely()
    assert shape.bounds == (-127.1631, 33.69, -117.0369, 41.71)


def test_event_contour_geopandas():
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    shape = message.gm.contours.to_dataframe()
    assert shape[shape.MMI == 5.0].PGA.values[0] == 65.7933


def test_event_map():
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')
    assert message.gm.map.fields[0].index == 1
    assert message.gm.map.fields[0].name == 'LON'
    assert message.gm.map.fields[0].units == 'deg'
    assert message.gm.map.grid[0] == [-126.8, 30.6, 0.001505, 0.055139, 1.0]


def test_event_map_geopandas():
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')
    message.gm.map.to_dataframe()


def test_event_contour_write():
    '''
    Test reading event read from file
    '''
    resource = io.StringIO()
    message = event.from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    # Change the value of our latitude to test if altering and writing works
    message.core.latitude.value = 10.0
    message.write(resource, format='xml')
    resource.seek(0)
    assert "<lat units=\"deg\">10.0</lat>" in resource.getvalue()

"""
..  codeauthor:: Charles Blais
"""
import pyshakealert.message.event as event


def test_event():
    """
    Test reading event read from file
    """
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    assert message.category == 'test'
    assert message.orig_sys == 'eqinfo2gm'
    assert message.message_type == 'new'
    assert message.version == 0
    assert message.timestamp == '1868-10-21T15:53:04.000Z'
    assert message.core_info.id == '1868_Hayward_M6.8'
    assert message.core_info.mag.value == 6.8
    assert message.core_info.mag.units == 'Mw'
    assert message.core_info.mag_uncer.value == 1.0
    assert message.core_info.mag_uncer.units == 'Mw'
    assert message.core_info.lat.value == 37.7
    assert message.core_info.lat_uncer.value == 0.5
    assert message.core_info.lon.value == -122.1
    assert message.core_info.lon_uncer.value == 0.5
    assert message.core_info.depth.value == 5
    assert message.core_info.depth_uncer.value == 50.0
    assert message.core_info.orig_time.value == '1868-10-21T15:53:00.000Z'
    assert message.core_info.orig_time_uncer.value == 20.0
    assert message.core_info.likelihood == 1.0
    assert message.core_info.num_stations == 0
    assert message.contributors.contributor[0].alg_name == 'dm'
    assert message.contributors.contributor[0].alg_version == '-'
    assert message.contributors.contributor[0].alg_instance == '-'
    assert message.contributors.contributor[0].category == 'test'
    assert message.contributors.contributor[0].event_id == '1868_Hayward_M6.8'
    assert message.contributors.contributor[0].version == 0


def test_event_contour():
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    assert message.gm_info.gmcontour_pred.contour[0].MMI.value == 2.0
    assert message.gm_info.gmcontour_pred.contour[0].PGA.value == 2.848
    assert message.gm_info.gmcontour_pred.contour[0].PGV.value == 0.2154
    assert message.gm_info.gmcontour_pred.contour[0].\
        polygon.coordinates[0] == [41.71, -122.1]


def test_event_contour_shapely():
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    shape = message.gm_info.gmcontour_pred.contour[0].polygon.to_shapely()
    assert shape.bounds == (-127.1631, 33.69, -117.0369, 41.71)


def test_event_contour_geopandas():
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    shape = message.gm_info.gmcontour_pred.to_dataframe()
    assert shape[shape.MMI == 5.0].PGA.values[0] == 65.7933


def test_event_map():
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')
    assert message.gm_info.gmmap_pred.grid_field[0].index == 1
    assert message.gm_info.gmmap_pred.grid_field[0].name == 'LON'
    assert message.gm_info.gmmap_pred.grid_field[0].units == 'deg'
    assert message.gm_info.gmmap_pred.grid[0] == [
        -126.8, 30.6, 0.001505, 0.055139, 1.0]


def test_event_map_geopandas():
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')
    message.gm_info.gmmap_pred.to_dataframe()


def test_event_contour_write():
    """
    Test reading event read from file
    """
    message = event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    # Change the value of our latitude to test if altering and writing works
    message.core_info.lat.value = 10.0
    content = event.to_string(message)
    print(content)
    assert '<lat units="deg">10.0</lat>' in content

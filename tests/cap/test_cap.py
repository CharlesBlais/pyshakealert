'''
..  codeauthor:: Charles Blais
'''
import pytest

from pyshakealert.message.event import from_file
from pyshakealert.cap.cap import eventToCap, NoCensusZoneFound
from pyshakealert.cap.census import Census


@pytest.fixture
def census():
    '''Create census object'''
    census = Census("pyshakealert/files/shapefiles/lcd_000a16a_e.zip")
    census_fr = Census("pyshakealert/files/shapefiles/ldr_000a16a_f.zip")
    census.merge_by_division_id(census_fr)
    return census


def test_cap(census):
    '''
    Read content of a valid contour file and test generation
    of a CAP message.  In this case, its in the US and we can't alert
    for that.
    '''
    # Load information
    event = from_file('tests/message/examples/SYN_CascadiaShallow_M9.3_00_contour.xml')
    message = eventToCap(event, census)
    assert len(message) > 0


def test_cap_out_of_zone(census):
    '''
    Read content of a valid contour file and test generation
    of a CAP message.  In this case, its in the US and we can't alert
    for that.
    '''
    event = from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')
    with pytest.raises(NoCensusZoneFound):
        eventToCap(event, census)


def test_cap_error(census):
    '''
    Read content of a valid contour file and test generation
    of a CAP message
    '''
    event = from_file('tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')
    with pytest.raises(ValueError):
        eventToCap(event, census)

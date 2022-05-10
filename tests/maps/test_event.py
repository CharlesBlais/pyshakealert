'''
..  codeauthor:: Charles Blais
'''
import pytest

import pyshakealert.message.event as event

import pyshakealert.maps.event as mapevent


@pytest.fixture
def sample() -> event.Event:
    """
    Test reading event read from file
    """
    return event.from_file(
        'tests/message/examples/1946Vancouver_contour.xml')


@pytest.fixture
def sample_map() -> event.Event:
    """
    Test reading event read from file
    """
    return event.from_file(
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_map.xml')


@pytest.mark.enable_socket
def test_contour(sample: event.Event):
    '''
    Test writing map
    '''
    mapevent.generate(sample)


@pytest.mark.enable_socket
def test_map(sample_map: event.Event):
    '''
    Test writing map
    '''
    mapevent.generate(sample_map)

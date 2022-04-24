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
        'tests/message/examples/Point_Source/1868_Hayward_M6.8_contour.xml')


def test_map(sample: event.Event):
    '''
    Test writing map
    '''
    mapevent.generate(sample, to_filename='test.png')
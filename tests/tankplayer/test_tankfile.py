'''
..  codeauthor:: Charles Blais
'''
import pytest

from pyshakealert.tankplayer import tankfile
from pyshakealert.config import get_app_settings


@pytest.mark.enable_socket
def test_tankfile_from_eventid():
    '''
    Tankfile from eventid
    '''
    settings = get_app_settings()
    tankgen = tankfile.TankGenerator(settings.fdsnws)
    tankgen.from_eventid('gsc2020lrjt', radius=1)
    assert False

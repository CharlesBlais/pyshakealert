"""
..  codeauthor:: Charles Blais
"""

from pyshakealert.tankplayer import tankfile


FDSNWS = 'http://sc3-stage.seismo.nrcan.gc.ca'


def test_tankfile_from_eventid():
    """
    Tankfile from eventid
    """
    tankgen = tankfile.TankGenerator(FDSNWS)
    tankgen.from_eventid('gsc2020lrjt')
    assert False

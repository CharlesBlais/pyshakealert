'''
Test :mod:`pyshakealert.channels.file`
======================================

Test chanfile library

..  codeauthor:: Charles Blais
'''
import io

# Third-party libraries
import pytest
from obspy import UTCDateTime
from obspy.clients.fdsn.client import Client

# User-contributed libraries
import pyshakealert.channels.file

# Constants
FDSNWS = 'http://fdsn.seismo.nrcan.gc.ca'


@pytest.fixture
def inventory():
    """
    Dummy inventory content using exsiting FDSNWS
    """
    client = Client(FDSNWS)
    return client.get_stations(
        network='CN',
        station='ORIO',
        channel='HN?',
        level='response',
        starttime=UTCDateTime())


def test_chanfile_create(inventory):
    """
    Test creation of chanfile
    """
    # Create StringIO that will hold our response
    resource = io.StringIO()
    # Generate the file in memory
    pyshakealert.channels.file.write(resource, inventory)
    # reset file pointer to 0
    resource.seek(0)
    # get the content
    content = resource.getvalue()
    assert '# 3 rows returned' in content

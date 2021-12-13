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
from pyshakealert.config import get_app_settings


@pytest.mark.enable_socket
def test_chanfile_create():
    """
    Test creation of chanfile
    """
    settings = get_app_settings()
    client = Client(settings.fdsnws)
    inventory = client.get_stations(
        network='CN',
        station='ORIO',
        channel='HN?',
        level='response',
        starttime=UTCDateTime())

    # Create StringIO that will hold our response
    resource = io.StringIO()
    # Generate the file in memory
    pyshakealert.channels.file.write(resource, inventory)
    # reset file pointer to 0
    resource.seek(0)
    # get the content
    content = resource.getvalue()
    print(content)
    assert '# 3 rows returned' in content

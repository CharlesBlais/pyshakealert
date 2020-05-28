"""
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

Test CAP alerting
=================

Pytest library for testing real-time alerting of EEW alerts.
"""


# User-contributed library
from pyshakealert.nads.client import FTP


def test_send():
    """
    Test the ability to generate a CAP message using the event information
    """
    client = FTP('naadsfeed2.pelmorex.com', username='nrcan', private_key='.ssh/pelmorex')
    client.send(open('tests/nads/examples/caps-example.xml').read())
    assert False

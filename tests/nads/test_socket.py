"""
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

Test CAP alerting
=================

Pytest library for testing real-time alerting of EEW alerts.
"""

import pytest
import logging

# User-contributed library
from pyshakealert.nads.socket import Socket


def test_socket():
    """
    Test the pelmorex socket
    """
    client = Socket()
    client.connect('streaming1.naad-adna.pelmorex.com', 8080, timeout=20)
    print(client.read())
    assert False

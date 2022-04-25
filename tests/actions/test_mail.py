'''
..  codeauthor:: Charles Blais
'''
import pytest

import logging

from unittest.mock import patch

import pyshakealert.message.event as event

from pyshakealert.actions.mail import Mailer


def mock_sendmail(_, from_addr, to_addrs, msg):
    logging.debug(f'[mock sendmail] from: {from_addr}')
    logging.debug(f'[mock sendmail] to: {to_addrs}')
    logging.debug(f'[mock sendmail] msg: {msg}')


@pytest.fixture
def sample() -> event.Event:
    """
    Test reading event read from file
    """
    return event.from_file(
        'tests/message/examples/1946Vancouver_contour.xml')


@patch('smtplib.SMTP.sendmail', mock_sendmail, create=True)
def test_mail(sample: event.Event):
    '''
    Test sending email of event
    '''
    mailer = Mailer(recipients=['charles.blais@nrcan-rncan.gc.ca'])
    mailer.send(sample)

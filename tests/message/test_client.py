"""
..  codeauthor:: Charles Blais
"""
import signal
import time
import datetime

import pytest

from pyshakealert.message.client import Client

# Constants
HOST = 'eew-cn-int1.seismo.nrcan.gc.ca'
USERNAME = 'system'
PASSWORD = 'FoziMz3PygYm'


@pytest.fixture
def client_dm():
    client = Client(HOST, port=61613)
    client.connect(username=USERNAME, password=PASSWORD)
    return client


@pytest.fixture
def client_sa():
    client = Client(HOST, port=62613)
    client.connect(username=USERNAME, password=PASSWORD)
    return client


@pytest.fixture
def fake_event():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<event_message category="live" message_type="new" orig_sys="dm" version="0" timestamp="{timestamp}Z">
  <core_info id="4557299">
    <mag units="Mw">6.4000</mag>
    <mag_uncer units="Mw">0.5000</mag_uncer>
    <lat units="deg">38.8000</lat>
    <lat_uncer units="deg">0.5000</lat_uncer>
    <lon units="deg">-122.8200</lon>
    <lon_uncer units="deg">0.5000</lon_uncer>
    <depth units="km">8.0000</depth>
    <depth_uncer units="km">5.0000</depth_uncer>
    <orig_time units="UTC">{timestamp}Z</orig_time>
    <orig_time_uncer units="sec">20.0000</orig_time_uncer>
    <likelihood>0.8000</likelihood>
    <num_stations>10</num_stations>
  </core_info>
  <contributors>
    <contributor alg_name="dm" alg_version="-" category="live" event_id="4557299" version="0"/>
  </contributors>
</event_message>
'''.format(timestamp=datetime.datetime.now().isoformat()[:19])


def test_listen(client_dm):
    """
    Test connection to client on heartbeat topic
    """
    # set signal handlers for stoping listener
    client_dm.listen('eew.sys.ha.data')
    time.sleep(10)


def test_listen_hb(client_sa):
    """
    Test connection to client on heartbeat topic
    """
    # set signal handlers for stoping listener
    client_sa.listen('eew.alg.finder.hb')
    time.sleep(10)



def test_send_hb(client_sa):
    """
    Test sending HB
    """
    fake_hb = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<hb originator="finder.eew-bk-int1" sender="finder.eew-bk-int1" timestamp="{timestamp}"/>
'''.format(
        timestamp=str(datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')))

    client_sa.send(
        'eew.alg.finder.hb',
        fake_hb.encode('utf-8'),
        expires=datetime.timedelta(seconds=10),
        message_type='hb_finder.eew-bk-int1')


def test_send(client_dm, fake_event):
    """
    Test connection to client
    """
    client_dm.send(
        'eew.sys.dm.data',
        fake_event.encode('utf-8'),
        expires=datetime.timedelta(seconds=10),
        message_type='new')

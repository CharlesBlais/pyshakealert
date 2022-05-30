"""
..  codeauthor:: Charles Blais
"""
import time
import datetime

import pytest

from pyshakealert.message.clients.mqtt import Client
from pyshakealert.config import get_app_settings


@pytest.fixture
def client() -> Client:
    settings = get_app_settings()
    client = Client(
        host=settings.amq_host,
        port=settings.amq_mqtt_port,
        username=settings.amq_username,
        password=settings.amq_password)
    return client


@pytest.fixture
def fake_event() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<event_message category="live" message_type="new" orig_sys="dm" \
version="0" timestamp="{timestamp}Z">
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
    <contributor alg_name="dm" alg_version="-" category="live" \
event_id="4557299" version="0"/>
  </contributors>
</event_message>
'''.format(timestamp=datetime.datetime.now().isoformat()[:19])


@pytest.mark.enable_socket
def test_message_listen_hb(client: Client):
    """
    Test connection to client on heartbeat topic
    """
    client.subscribe('#')
    time.sleep(10)
    client.disconnect()


def test_message_send_hb(client: Client):
    """
    Test sending HB
    """
    fake_hb = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<hb originator="finder.eew-bk-int1" sender="finder.eew-bk-int1" \
timestamp="{timestamp}"/>
'''.format(
        timestamp=str(
            datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
        )

    client.subscribe('#')
    time.sleep(5)
    client.publish('eew/alg/finder/hb', fake_hb)
    time.sleep(5)
    client.disconnect()


def test_message_send(client: Client, fake_event: str):
    """
    Test connection to client
    """
    client.subscribe('#')
    time.sleep(5)
    client.publish('eew/sys/dm/data', fake_event)
    time.sleep(5)
    client.disconnect()

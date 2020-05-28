"""
..  codeauthor:: Charles Blais
"""
import os
import subprocess
import tempfile
import logging

# Third-party applications
from obspy import Stream
from obspy.clients.fdsn import Client
from obspy.core.event.event import Event
from obspy.clients.fdsn.header import FDSNNoDataException

# Constants
DEFAULT_MS2TANK = '/app/eewdata/ew/bin/ms2tank'
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_PAD_BEFORE = 60  # seconds
DEFAULT_PAD_AFTER = 600  # seconds


class TankException(Exception):
    """Tankfile exception"""


class EmptyEventException(Exception):
    """Empty event exception"""


def from_mseed_file(
    filename: str,
    application: str = DEFAULT_MS2TANK,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """
    Convert miniseed file to tank file using application
    """
    if not os.path.exists(application):
        raise TankException(f'Could not find {application}')
    if not os.path.exists(filename):
        raise TankException(f'Tank input mseed {filename} does not exist')
    logging.info(f'Converting mseed to tank: {application} {filename}')
    return subprocess.check_output(
        [application, filename], timeout=DEFAULT_TIMEOUT)


def from_stream(
    stream: Stream,
    **kwargs,
) -> bytes:
    """
    Convert stream to tank file

    :see: from_mseed_file
    """
    fp = tempfile.NamedTemporaryFile(mode='wb')
    stream.write(fp.name, format='MSEED', reclen=512, encoding='STEIM2')
    return from_mseed_file(fp.name, **kwargs)


class TankGenerator(object):
    """
    Using an FDSNWS client, we generate a file based on teh catalogue
    object or a and event found in the FDSNWS.

    Routines grab the pick in the event and pad the result

    :param str fdsnws: fdsn client url
    :param str application: application for ms2tank
    :param int timeout: timeout for calling applications
    """
    def __init__(
        self,
        fdsnws: str,
        application: str = DEFAULT_MS2TANK,
        timeout: int = DEFAULT_TIMEOUT
    ):
        self.client = Client(fdsnws)
        self.application = application
        self.timeout = timeout

    def from_event(
        self,
        event: Event,
        pad_before: int = DEFAULT_PAD_BEFORE,
        pad_after: int = DEFAULT_PAD_AFTER,
    ) -> bytes:
        """
        Convert and obspy event to tankfile
        """
        logging.info(f'Processing event {event}')
        if not len(event.picks):
            raise EmptyEventException('No picks found in the event')
        times = [pick.time for pick in event.picks]
        starttime = min(times) - pad_before
        endtime = max(times) + pad_after

        stream = Stream()
        # Get the data from the pick information
        for pick in event.picks:
            logging.info(f'Download data for {pick.waveform_id.network_code}.\
{pick.waveform_id.station_code}.{pick.waveform_id.location_code}.\
{pick.waveform_id.channel_code} \
from {starttime} to {endtime}')
            try:
                stream += self.client.get_waveforms(
                    network=pick.waveform_id.network_code,
                    station=pick.waveform_id.station_code,
                    location=pick.waveform_id.location_code,
                    channel=pick.waveform_id.channel_code,
                    starttime=starttime,
                    endtime=endtime,
                )
            except FDSNNoDataException as err:
                logging.warning(err)
        return from_stream(
            stream, application=self.application, timeout=self.timeout)

    def from_eventid(
        self,
        eventid: str,
        **kwargs
    ) -> bytes:
        """
        Query the FDSNWS from an eventid and extract
        all picks

        :param str eventid: event id
        """
        logging.info(f'Getting data for event id: {eventid}')
        catalogue = self.client.get_events(
            eventid=eventid, includearrivals=True)
        return self.from_event(catalogue.events[0], **kwargs)

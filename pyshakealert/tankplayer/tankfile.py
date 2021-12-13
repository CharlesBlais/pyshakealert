"""
..  codeauthor:: Charles Blais
"""
import os
import subprocess
import tempfile
import logging
import datetime
from typing import Optional, Union

# Third-party applications
from obspy import Stream, UTCDateTime
from obspy.clients.fdsn import Client
from obspy.core.event.event import Event
from obspy.clients.fdsn.header import FDSNNoDataException

from pyshakealert.exceptions import TankException, EmptyEventException
from pyshakealert.config import get_app_settings


settings = get_app_settings()


def from_mseed_file(
    filename: str,
    app: str = settings.ms2tank,
    timeout: int = settings.ms2tank_timeout,
) -> bytes:
    """
    Convert miniseed file to tank file using application
    """
    if not os.path.exists(app):
        raise TankException(f'Could not find {app}')
    if not os.path.exists(filename):
        raise TankException(f'Tank input mseed {filename} does not exist')
    logging.info(f'Converting mseed to tank: {app} {filename}')
    return subprocess.check_output([app, filename], timeout=timeout)


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


def split_stream(
    stream: Stream,
    buffer_size: float
) -> Stream:
    """
    Split stream traces by the buffer size and sort all of them by
    the starttime
    """
    # no data, no splitting
    if len(stream) == 0:
        return stream

    # get the starttime to start the splitting
    starttime = min([trace.stats.starttime for trace in stream])
    endtime = max([trace.stats.endtime for trace in stream])

    stream_split = Stream()
    current = starttime
    while current < endtime:
        for trace in stream:
            subtrace = trace.slice(
                starttime=current,
                endtime=current + buffer_size - trace.stats.delta
            )
            if len(subtrace.data) != 0:
                stream_split.append(subtrace)
        current += buffer_size
    return stream_split


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
        fdsnws: str = settings.fdsnws,
        timeout: int = settings.ms2tank_timeout
    ):
        self.client = Client(fdsnws)
        self.timeout = timeout

    def from_event(
        self,
        event: Event,
        radius: Optional[float] = None,
        pad_before: float = settings.ms2tank_pad_before,
        pad_after: float = settings.ms2tank_pad_after,
        buffer_size: float = settings.ms2tank_buffer_size,
        force_starttime: Optional[
            Union[datetime.datetime, UTCDateTime]] = None,
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

        if radius is None:
            stations = [{
                'network': pick.waveform_id.network_code,
                'station': pick.waveform_id.station_code,
                'location': pick.waveform_id.location_code,
                'channel': pick.waveform_id.channel_code,
            } for pick in event.picks]
        else:
            inv = self.client.get_stations(
                starttime=starttime,
                endtime=endtime,
                latitude=event.origins[0].latitude,
                longitude=event.origins[0].longitude,
                maxradius=radius,
                level='channel',
            )
            stations = [{
                'network': network.code,
                'station': station.code,
                'location': channel.location_code,
                'channel': channel.code,
            } for network in inv for station in network for channel in station]

        # Get the data from the pick information
        stream = Stream()
        for station in stations:
            logging.info(
                'Download data for {network}.{station}.{location}.{channel} \
from {starttime} to {endtime}'.format(
                    starttime=starttime,
                    endtime=endtime,
                    **station))
            try:
                stream += self.client.get_waveforms(
                    starttime=starttime,
                    endtime=endtime,
                    **station,
                )
            except FDSNNoDataException as err:
                logging.warning(err)

        # Correct the startttime of the streams if its set
        logging.info(f'Stream before offset: {stream}')
        offset = 0
        if isinstance(force_starttime, datetime.datetime):
            offset = UTCDateTime(force_starttime) - starttime
        elif isinstance(force_starttime, UTCDateTime):
            offset = force_starttime - starttime
        logging.info(f'Offsetting results with {offset} seconds')
        for trace in stream:
            trace.stats.starttime += offset
        logging.info(f'Stream after offset: {stream}')

        # Split the stream by buffer size for the tankfile, the streams
        # need to be small and in small buffer sizes for tankfile playback
        stream = split_stream(stream, buffer_size)

        return from_stream(
            stream,
            timeout=self.timeout)

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

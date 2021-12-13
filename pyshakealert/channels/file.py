"""
Channel file library
====================

Library for creating channel file using FDSN-WS response.  The channel file
supports any seismic channels.  The mandatory information present in the
response must be:

    - network code
    - station code
    - location code
    - channel code
    - latitude
    - longitude
    - elevation
    - sample_rate (Hz)
    - gain
    - units
    - ground motion clip
    - channel azimuth
    - channel dip
    - channel description

It is currently unknown if the channel description is a mandatory field.

..  codeauthor:: Charles Blais
"""
import datetime
from typing import Union, Optional, TextIO

# Third-party libraries
from obspy.core.inventory.inventory import Inventory

from pyshakealert.config import get_app_settings


def write(
    filename: Union[str, TextIO],
    inventory: Inventory,
    user: Optional[str] = None
) -> None:
    """
    Using a obspy inventory object (with response level information) we use
    the Jinja2 template the create the file.

    :type filename: str or resource
    :param filename: file to write to
    :type inventory: :class:`obspy.core.inventory.Inventory`
    :param inventory: list of channel
    :param str user: user name signature (optional)
    """
    settings = get_app_settings()

    resource = open(filename, 'w') if isinstance(filename, str) else filename

    # Recalculate overall sensitivity of all channnels
    for network in inventory:
        for station in network:
            for channel in station:
                channel.response.recalculate_overall_sensitivity()

    resource.write(settings.template_chanfile.render(
        now=datetime.datetime.now(),
        user='unknown' if not user else user,
        inventory=inventory
    ))

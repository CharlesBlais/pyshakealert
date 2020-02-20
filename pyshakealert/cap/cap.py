'''
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

CAP Message Generator
=====================

Library for handling earthquake early warning (EEW) CAP alerting messages.
The following is based on the documentation found at:

    http://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html

In this code, it handles EEW message as event_message received through
ShakeAlert decision module.

Using Jinja2 template, we generate the CAP message.  The Jinja2 template
contains conditions to generate the message.
'''
import datetime
import logging
from pkg_resources import resource_filename

# Third-party libraries
from jinja2 import Environment, FileSystemLoader

# User-contributed libraries
from pyshakealert.message.event import Event
from pyshakealert.cap.census import Census

# Constants
JINJA2_ENV = Environment(
    loader=FileSystemLoader(
        resource_filename('pyshakealert', 'files/templates')
    ), trim_blocks=True
)
CAP_TEMPLATE = 'cap.xml'


class NoCensusZoneFound(Exception):
    '''Custom exception for no census zone found'''


def eventToCap(
    event: Event,
    census: Census,
    status: str = 'Test',
    minmmi: int = 0,
):
    '''
    Convert an earthquake early warning event to CAP as string

    The received event must contain contour information in order
    to determine the zone impact.

    :type event: :class:`pyshakealert.message.event.Event`
    :param event: Event message received through decision module

    :type census: :class:`pyshakealert.cap.census.Census`
    :param census: Census information

    :param int minmmi: Minimum MMI to send a CAP alert for (default is smallest)

    :param str status: status of the CAP message
    :rtype: str

    :raise NoCensusZoneFound: no census zone found in message
    :raise ValueError: invalid status sent or contour found
    '''
    allowed_cap_status = ['Actual', 'Exercise', 'System', 'Test', 'Draft']
    if status not in allowed_cap_status:
        raise ValueError("Invalid status %s, must be %s" % (status, ", ".join(allowed_cap_status)))

    # Extrac the single contour information we need to send an alert, we simply
    # get the contour with the matching MMI and extract its polygon information.
    logging.info("Searching for smaller MMI contout >= %s", minmmi)
    mycontour = None
    for contour in event.gm.contours:
        if contour.mmi.value < minmmi:
            logging.debug("Contour MMI %s < %s - ignore", contour.mmi.value, minmmi)
            # too small to send a mesage
            continue
        elif contour.mmi.value == minmmi:
            logging.debug("Contour MMI %s = %s - found", contour.mmi.value, minmmi)
            # we found our exact contour
            mycontour = contour
            break
        elif mycontour is None or mycontour.mmi.value > contour.mmi.value:
            logging.debug("Contour MMI %s > %s", contour.mmi.value, minmmi)
            mycontour = contour
    if not mycontour:
        raise ValueError("There may no contour in the event message or \
none are below are above the MMI of %d" % minmmi)

    # Grab all the census divison that intersect our contour (english only)
    # For the french, we just assume thar are census object contain the same
    # information but just different names.
    polygon = mycontour.polygon.to_shapely()
    logging.info("Finding english census zones the intersect %s", polygon)
    zone = census.get_census_divisions(polygon)
    if zone.empty:
        raise NoCensusZoneFound("Could not find any english census zone for %s" % str(polygon))
    logging.info("Found the following matches: %s", str(zone))

    logging.info("Generate CAP using template %s", CAP_TEMPLATE)
    return JINJA2_ENV.get_template(CAP_TEMPLATE).render(
        event=event,
        locations=sorted(zone['CDUID'].tolist()),
        area=mycontour.polygon['#text'],  # get the raw form polygon
        areas_en=sorted(zone['CDNAME'].tolist()),
        areas_fr=sorted(zone['DRNOM'].tolist()),
        sent=datetime.datetime.now(),
        wpamexpire=datetime.datetime.now() + datetime.timedelta(minutes=15),
        expires=datetime.datetime.now() + datetime.timedelta(minutes=30),
        status=status
    )

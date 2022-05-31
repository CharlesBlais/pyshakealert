"""
Mail client
===========

Mail client for sending event message information with optional map and grids
as body content.

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
import logging

from typing import List

import smtplib

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.mime.base import MIMEBase

from email import encoders

from dateutil.parser import parse

from .models import Client, Event

from pyshakealert.config import get_app_settings

from pyshakealert.message.event import to_string

from pyshakealert.maps.event import generate


class Mailer(Client):
    '''
    General wrapper for emailer

    :type recipients: [str]
    :param recipients: list of email clients
    '''
    def __init__(
        self,
        recipients: List[str] = []
    ):
        self.recipients = recipients

    @staticmethod
    def _event_to_subject(event: Event) -> str:
        '''
        Convert the event to a subject

        :type event: :class:`pyshakealert.message.event.event.Event`
        :param event: event information
        '''
        return f'ShakeAlert: {event.core_info.mag.value} {event.core_info.mag.units} \
at {event.timestamp} from {event.instance}'

    def send(
        self,
        event: Event,
    ) -> bool:
        '''
        At this stage, we have usually determined we can send an email

        From the configuration, we grab the template file and list of emails

        :type event: :class:`pyshakealert.message.event.event.Event`
        :param event: event information
        :rtype: bool
        :returns: success or not
        '''
        settings = get_app_settings()

        subject = Mailer._event_to_subject(event)

        proc_time = parse(event.timestamp)
        origin_time = parse(event.core_info.orig_time.value)
        delta_seconds = (proc_time - origin_time).total_seconds()

        body = settings.template_mail.render(
            event=event,
            delta_seconds=delta_seconds)

        eventxml = MIMEApplication(to_string(event), Name='event.xml')
        eventxml['Content-Disposition'] = 'attachment; filename="event.xml"'

        image = MIMEBase('image', 'png', filename='map.png')
        image.add_header(
            'Content-Disposition', 'attachment', filename='map.png')
        image.add_header('X-Attachment-Id', 'map')
        image.add_header('Content-ID', '<map>')
        image.set_payload(generate(event))
        encoders.encode_base64(image)

        logging.info(f"Sending email {subject} to {self.recipients} \
via {settings.smtp_server}")
        logging.debug(body)
        # Create SMTP handler
        s = smtplib.SMTP(settings.smtp_server)
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.email_from
        msg['To'] = ", ".join(self.recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        msg.attach(eventxml)
        msg.attach(image)
        # Send the message via our own SMTP server.
        s.sendmail(msg['From'], self.recipients, msg.as_string())
        # Quit from handler
        s.quit()
        return True

'''
..  codeauthor:: Charles Blais
'''
import logging

from typing import List

import base64

import smtplib

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from dateutil.parser import parse

from .models import Client, Event

from pyshakealert.config import get_app_settings

from pyshakealert.message.event import to_string

from pyshakealert.maps.event import generate


class Mailer(Client):
    '''
    General wrapper for emailer
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
        '''
        return f'ShakeAlert Event at {event.timestamp} from {event.instance}'

    def send(
        self,
        event: Event,
    ) -> bool:
        '''
        At this stage, we have usually determined we can send an email

        From the configuration, we grab the template file and list of emails

        Additional kwargs can be sent to the Jinja template using kwargs
        '''
        settings = get_app_settings()

        subject = Mailer._event_to_subject(event)

        proc_time = parse(event.timestamp)
        origin_time = parse(event.core_info.orig_time.value)
        delta_seconds = (proc_time - origin_time).total_seconds()

        image = base64.encodebytes(generate(event)).decode('utf-8')

        body = settings.template_mail.render(
            event=event,
            image=image,
            delta_seconds=delta_seconds)

        part = MIMEApplication(to_string(event), Name='event.xml')
        part['Content-Disposition'] = 'attachment; filename="event.xml"'

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
        msg.attach(part)
        # Send the message via our own SMTP server.
        s.sendmail(msg['From'], self.recipients, msg.as_string())
        # Quit from handler
        s.quit()
        return True

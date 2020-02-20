'''
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

Pelmorex sender library for FTP
===============================

Send pelmorex CAP message to pelmorex
'''
import os
import logging
import tempfile
import datetime
from typing import Optional, Union

# Third-party library
import pysftp


class FTP(object):
    '''
    Sender handle for sending data to Pelmorex.

    :param str host: host URL
    :param str username: username for FTP
    :param str private_key: file for privateKey
    :param str destination: destination directory on the FTP (default: cap)
    '''
    def __init__(
        self,
        hostname: str,
        username: str,
        private_key: str,
        destination: str = 'cap',
    ) -> None:
        self.hostname = hostname
        # destination directory at the source
        self.destination = destination

        self.sftp = pysftp.Connection(
            self.hostname,
            username=username,
            private_key=private_key)

    def send(
        self,
        cap_message: Union[str, bytes],
        event_id: Optional[str] = None,
    ) -> None:
        '''
        Send events to pelmorex (NADS) to configured directory

        :param str cap_message: XML format CAP message
        :param str event_id: used for destination filename (default: YmdHisf)
        '''
        if event_id is None:
            event_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            logging.debug("No event_id specified, using %s", event_id)

        # Save the cap_message into a temporary file for the FTP
        # file transfer
        fp = tempfile.TemporaryFile(encoding='utf-8')
        if isinstance(cap_message, str):
            cap_message = cap_message.encode('utf-8')
        fp.write(cap_message)
        fp.seek(0)
        ftpfile = os.path.join(self.destination, "{0}.xml".format(event_id))

        logging.info(
            "Sending CAP message to %s from %s to %s",
            self.hostname, fp.name, ftpfile
        )

        # Gather statistical information while sending
        before = datetime.datetime.now()

        # Send the content
        attr = self.sftp.put(fp.name, remotepath=ftpfile)

        # Gather additional statistical information
        after = datetime.datetime.now()
        after_host = datetime.datetime.fromtimestamp(attr.st_mtime)

        logging.debug("Sent message at %s", before.isoformat())
        logging.debug("Message received at %s", after.isoformat())
        logging.debug("According to host %s", after_host.isoformat)
        logging.debug("Difference %s", str(after - before))
        logging.debug("Difference from host %s", str(after_host - before))

"""
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

Pelmorex sender library for FTP
===============================

Send pelmorex CAP message to pelmorex
"""
import os
import logging
import tempfile
import datetime
from typing import Optional, Union

# Third-party library
from paramiko import SSHClient, AutoAddPolicy

# Constants
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_DESTINATION = 'cap'


class FTP(object):
    """
    Sender handle for sending data to Pelmorex.

    :param str host: host URL
    :param str username: username for FTP
    :param str private_key: file for privateKey
    :param str destination: destination directory on the FTP (default: cap)
    """
    def __init__(
        self,
        hostname: str,
        username: str,
        private_key: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        # Initiate SSH tunnel with SCP
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())

        logging.info(f'Initiating connection to {username}@{hostname} \
with key {private_key}')
        client.connect(
            hostname, username=username,
            key_filename=private_key, look_for_keys=True, timeout=timeout)
        self.sftp = client.open_sftp()

    def send(
        self,
        cap_message: Union[str, bytes],
        event_id: Optional[str] = None,
        destination: str = DEFAULT_DESTINATION,
    ) -> None:
        """
        Send events to pelmorex (NADS) to configured directory

        :param str cap_message: XML format CAP message
        :param str event_id: used for destination filename (default: YmdHisf)
        """
        if event_id is None:
            event_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            logging.debug(f'No event_id specified, using {event_id}')

        # Save the cap_message into a temporary file for the FTP
        # file transfer
        fp = tempfile.TemporaryFile(encoding='utf-8')
        if isinstance(cap_message, str):
            cap_message = cap_message.encode('utf-8')
        fp.write(cap_message)
        fp.seek(0)
        ftpfile = os.path.join(destination, f'{event_id}.xml')

        logging.info(f'Sending CAP message to NADS from \
{fp.name} to {ftpfile}')

        # Gather statistical information while sending
        before = datetime.datetime.now()

        # Send the content
        attr = self.sftp.put(fp.name, remotepath=ftpfile)

        # Gather additional statistical information
        after = datetime.datetime.now()
        after_host = datetime.datetime.fromtimestamp(attr.st_mtime)

        logging.debug(f'Sent message at {before.isoformat()}')
        logging.debug(f'Message received at {after.isoformat()}')
        logging.debug(f'According to host {after_host.isoformat()}')
        logging.debug(f'Difference {after - before}')
        logging.debug(f'Difference from host {after_host - before}')

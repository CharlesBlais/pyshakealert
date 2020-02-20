'''
..  codeauthor:: Charles Blais <charles.blais@canada.ca>

Pelmorex sender library for FTP
===============================

Send pelmorex CAP message to pelmorex
'''
import socket
import io
import logging
from lxml import etree
from typing import Optional


class InvalidCapMessage(Exception):
    '''Invalid CAP message received'''


class Socket(object):
    '''
    TCP socket client that listens to messages send via socket

    :type sock: class:`socket.Socket`
    :param sock: socket connection
    '''
    def __init__(
        self,
        sock: Optional[socket.SocketIO] = None
    ) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if sock is None else sock

    def connect(
        self,
        host: str,
        port: int = 8080,
        timeout: int = 120
    ):
        '''
        Start the connection to the host.  Note, according to pelmorex
        documentation there is a hearthbeat sent each minute on the
        socket connection.

        :param str host: host IP
        :param int port: port to connect to (default: 8080)
        :param int timeout: connection timeout in seconds (default: 120)

        :raise InvalidCapMessage: invalid format CAP message received
        '''
        self.sock.settimeout(timeout)
        logging.info("Connecting to %s port %d" % (host, port))
        self.sock.connect((host, port))

    def read(self, attempts=20):
        '''
        Read the content of the message buffer at a max size of 2048
        Read its content buffer at a maximum of x times in case the content
        of the buffer never terminates.

        We assume buffer termination with the character </alert> but this does
        not guarantee that the message is well formed.

        :throws InvalidPelmorexMessage: invalid pelmorex message received

        :rtype: :class:`xml.etree.ElementTree`
        :return: CAP message as XML
        '''
        buff = io.StringIO()
        for attempt in range(attempts):
            logging.info("Waiting %d..." % attempt)
            data = str(self.sock.recv(32768), 'utf-8')
            logging.info("Received %s" % data)
            buff.write(data)
            # stop at </alert> pattern
            if '</alert>' in buff.getvalue():
                break

        # if we had reach the end of the attempts, throw an error
        # this can be caused from the message block too big
        if attempt == 9:
            raise InvalidCapMessage(
                "Invalid CAP message: %s" % buff.getvalue()
            )

        logging.info("Message complete")
        try:
            return etree.fromstring(bytes(buff.getvalue(), encoding='utf-8'))
        except etree.XMLSyntaxError as err:
            raise InvalidCapMessage(err)

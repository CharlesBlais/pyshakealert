"""
Message client
===============

ActiveMQ client that abstract the behind-the-scene message passing
protocol.  We try, as much as we can, to abstract the use of STOMP
protocol so that future message broker upgrades wont' be impacted.

..  codeauthor:: Charles Blais
"""
import datetime
import logging
from typing import List, Union, Optional, Callable, Tuple

# Third-party library
import stomp

from pyshakealert.exceptions import \
    ConnectFailedException, MissingCredentialsException

from pyshakealert.config import get_app_settings

settings = get_app_settings()


class Client:
    """
    Client wrapper for stomp protocol used by ActiveMQ client
    """
    def __init__(
        self,
        host: Union[str, List[str]],
        port: Union[int, List[int]] = 61613,
        username: str = '',
        password: str = '',
        keepalive: bool = False,
        heartbeats: Tuple[int, int] = (0, 0),
    ) -> None:
        """
        In the case of stomp, multiple host and port can be defined.  If the
        host is an array, then the port for a single value or a list of
        same length.

        .. note::
            When used, the heart-beat header MUST contain two positive integers
            separated by a comma. The first number represents what the sender
            of the frame can do (outgoing heart-beats):

                0 means it cannot send heart-beats

            otherwise it is the smallest number of milliseconds between
            heart-beats that it can guarantee. The second number represents
            what the sender of the frame would like to get (incoming
            heart-beats):

                0 means it does not want to receive heart-beats

            otherwise it is the desired number of milliseconds between
            heart-beats

        :type host: str or list
        :param host: host to connect to

        :type port: int or list
        :param port: port to connect

        :param str username: username cred
        :param str password: password cred

        :param bool keepalive: send keepalive signal for permanent connection

        :param Tuple[int, int] heartbeats: see note

        :raise ValueError: bad inputs
        :raise ConnectFailedException: unable to connect
        """
        # transform and validate host and port
        if isinstance(host, list) and isinstance(port, list):
            if len(host) != len(port):
                raise ValueError('host and port must be of same length')
            host_and_port = list(zip(host, port))
        elif isinstance(host, list) and isinstance(port, int):
            host_and_port = list(zip(host, [port]*len(host)))
        elif isinstance(host, str) and isinstance(port, int):
            host_and_port = [(host, port)]
        else:
            raise ValueError('Incompatible type sent to host and port')

        # Establish connection and set defaults
        self.username = username
        self.password = password
        self.topic: Optional[str] = None
        self.subscription_id: Optional[str] = None

        logging.info(f'Initiate connection to {host_and_port}')
        self.conn = stomp.Connection(
            host_and_port,
            auto_content_length=False,
            keepalive=keepalive,
            heartbeats=heartbeats)

    def connect(self) -> None:
        """
        Establish connection

        .. note::
            For stomp, username and password are also required.  They are
            keywords since certain protocols may not require credentials.

        :raise MissingCredentialsException: failed to provide username
            and password
        :raise ConnectFailedException: failed to connect
        """
        if self.username == '' or self.password == '':
            raise MissingCredentialsException('username and password \
must be set for stomp')

        try:
            logging.info(f"Connection to broker with user {self.username}")
            self.conn.connect(self.username, self.password, wait=True)
        except stomp.exception.ConnectFailedException as err:
            raise ConnectFailedException(err)

    def disconnect(self) -> None:
        """
        Disconnect from the connection
        """
        self.conn.disconnect()

    def listen(
        self,
        topic: str,
        subscription_id: Optional[str] = None,
        listener: Optional[Callable] = None
    ) -> None:
        """
        Subcribe to the topic sent and listen for messages

        A default listenery is set using MyDefaultListener which just outputs
        the content of the message to stdout.  The listener must follow
        the same template.

        If the subscription_id is not set, we use the username as the default.

        ..  note::
            This routine is non-blocking.  Although we exit the routine, the
            thread is still running until the object is destroyed

        :param str topic: ActiveMQ topic to subcribe too
        :param str subscription_id: connection id (use username by default)
        :param object listener: add custom listener according to stomp.py doc

        :raise ConnectFailedException: connection not initiated
        """
        if not self.conn.is_connected():
            raise ConnectFailedException('Must be connected to ActiveMQ to \
listen, use connect')

        # set the subcription id if not set
        if subscription_id is None:
            logging.debug(f'subcription not defined, using \
username {self.username}')
            subscription_id = self.username

        if listener is not None:
            logging.info(f'Adding custom message listener {listener}')
            self.conn.set_listener('', listener)

        # save information
        self.topic = topic
        self.subscription_id = subscription_id

        logging.info(f'Subscribing to topic {self.topic}')
        self.conn.subscribe(self.topic, self.subscription_id)

    def reconnect(self):
        '''
        Use saved information to re-establish our connection
        '''
        if self.conn.is_connected():
            logging.info('Client is already connected')
            return None

        # restart connection
        self.connect()
        logging.info(f'Re-subscribing to topic {self.topic}')
        self.conn.subscribe(self.topic, self.subscription_id)

    def send(
        self,
        topic: str,
        body: Union[str, bytes],
        content_type: Optional[str] = None,
        expires: float = settings.message_expires,
        message_type: Optional[str] = None,
        message_id: int = 1,
    ) -> None:
        """
        Send a message to the ActiveMQ broker

        It is assumed that all message are in UTF-8

        :param str topic: topic to sent to
        :param str body: body content
        :param str content_type: optional header for content-type
        :type expires: :class:`datetime.datetime`
            or :class:`datetime.timedelta`
        :param expires: time the message should expire
        :param message_type: adds custom ShakeAlert type header to the message
        :param message_id: adds custom ShakeAlert sequence ID to the message

        :raise ConnectFailedException: connection not initiated
        """
        if not self.conn.is_connected():
            raise ConnectFailedException('Must be connected to ActiveMQ to \
listen, use connect')

        # Create header information
        headers = {
            'timestamp': "%d" % int(datetime.datetime.now().timestamp()*1000),
            'id': message_id
        }
        if message_type is not None:
            headers['type'] = message_type

        headers['expires'] = "%d" % int((
            datetime.datetime.now() + datetime.timedelta(seconds=expires)
        ).timestamp()*1000)

        logging.info(f'Sending message to broker topic {topic} \
with header: {headers}')
        self.conn.send(
            destination=topic,
            body=body.encode('utf-8') if isinstance(body, str) else body,
            content_type=content_type,
            headers=headers,
        )

'''
Message client
===============

ActiveMQ client that abstract the behind-the-scene message passing
protocol.

..  codeauthor:: Charles Blais
'''
import datetime
import logging
from typing import List, Union, Optional, Callable

# Third-party library
import stomp

# Every message sent have a default expire time defined as a timedelta
DEFAULT_EXPIRE = datetime.timedelta(seconds=600)


class ConnectFailedException(stomp.exception.ConnectFailedException):
    '''Custom exception'''


class MissingCredentialsException(Exception):
    '''Missing credentials'''


class Client():
    '''
    Client wrapper for stomp protocol used by ActiveMQ client
    '''
    def __init__(
        self,
        host: Union[str, List[str]],
        port: Union[int, List[int]] = 61613,
    ) -> None:
        '''
        Constructor that establishes the connection to the ActiveMQ broker

        In the case of stomp, multiple host and port can be defined.  If the host
        is an array, then the port for a single value or a list of same length.

        :type host: str or list
        :param host: host to connect to

        :type port: int or list
        :param port: port to connect

        :raise ValueError: bad inputs
        :raise ConnectFailedException: unable to connect
        '''
        # transform and validate host and port
        if isinstance(host, list) and isinstance(port, list):
            if len(host) != len(port):
                raise ValueError("host and port must be of same length")
            host_and_port = list(zip(host, port))
        elif isinstance(host, list) and isinstance(port, int):
            host_and_port = list(zip(host, [port]*len(host)))
        elif isinstance(host, str) and isinstance(port, int):
            host_and_port = [(host, port)]
        else:
            raise ValueError("Incompatible type sent to host and port")

        # Establish connection and set defaults
        self.username: str = ''
        self.password: str = ''
        logging.info("Initiate connection to %s", str(host_and_port))
        self.conn = stomp.Connection(
            host_and_port,
            auto_content_length=False)

    def connect(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> None:
        '''
        Establish connection

        For stomp, username and password are also required.  They are keywords since
        certain protocols may not require credentials.

        :param str username: username credentials
        :param str password: password credentials

        :raise MissingCredentialsException: failed to provide username and password
        :raise ConnectFailedException: failed to connect
        '''
        if username is None or password is None:
            raise MissingCredentialsException("username and password must be set for stomp")

        # save information
        self.username = username
        self.password = password

        try:
            logging.info("Connection to broker with user %s", self.username)
            self.conn.connect(self.username, self.password, wait=True)
        except stomp.exception.ConnectFailedException as err:
            raise ConnectFailedException(err)

    def disconnect(self) -> None:
        '''
        Disconnect from the connection
        '''
        self.conn.disconnect()

    def listen(
        self,
        topic: str,
        subscription_id: Optional[str] = None,
        listener: Optional[Callable] = None
    ) -> None:
        '''
        Subcribe to the topic sent and listen for messages

        A default listenery is set using MyDefaultListener which just outputs
        the content of the message to stdout.  The listener must follow
        the same template.

        If the subscription_id is not set, we use the username as the default.

        ..  note:: This routine is non-blocking

        :param str topic: ActiveMQ topic to subcribe too
        :param str subscription_id: connection id (use username by default)
        :param object listener: add custom listener according to stomp.py doc

        :raise ConnectFailedException: connection not initiated
        '''
        if not self.conn.is_connected():
            raise ConnectFailedException("Must be connected to ActiveMQ to listen, use connect")

        # set the subcription id if not set
        if subscription_id is None:
            logging.debug("subcription not defined, using username %s", self.username)
            subscription_id = self.username

        if listener is not None:
            logging.info("Adding custom message listener %s", str(listener))
            self.conn.set_listener('', listener)
        logging.info("Subscribing to topic %s", topic)
        self.conn.subscribe('/topic/%s' % topic, subscription_id)
        # although we exit the routine, the thread is still running until
        # the object is destroyed

    def send(
        self,
        topic: str,
        body: Union[str, bytes],
        content_type: Optional[str] = None,
        expires: Union[datetime.datetime, datetime.timedelta] = DEFAULT_EXPIRE,
        message_type: Optional[str] = None,
        message_id: int = 1,
    ) -> None:
        '''
        Send a message to the ActiveMQ broker

        It is assumed that all message are in UTF-8

        :param str topic: topic to sent to
        :param str body: body content
        :param str content_type: optional header for content-type
        :type expires: :class:`datetime.datetime` or :class:`datetime.timedelta`
        :param expires: time the message should expire
        :param message_type: adds custom ShakeAlert type header to the message
        :param message_id: adds custom ShakeAlert sequence ID to the message

        :raise ConnectFailedException: connection not initiated
        '''
        if not self.conn.is_connected():
            raise ConnectFailedException("Must be connected to ActiveMQ to listen, use connect")

        # Create header information
        headers = {
            'timestamp': "%d" % int(datetime.datetime.now().timestamp()*1000),
            'id': message_id
        }
        if message_type is not None:
            headers['type'] = message_type

        if isinstance(expires, datetime.datetime):
            headers['expires'] = "%d" % int(expires.timestamp()*1000)
        else:
            headers['expires'] = "%d" % int((datetime.datetime.now() + expires).timestamp()*1000)

        logging.info("Sending message to broker topic %s with header: %s", topic, str(headers))
        self.conn.send(
            destination='/topic/%s' % topic,
            body=body.encode('utf-8') if isinstance(body, str) else body,
            content_type=content_type,
            headers=headers,
        )

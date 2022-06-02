"""
Message client
===============

ActiveMQ client that abstract the behind-the-scene message passing
protocol.  We try, as much as we can, to abstract the use of MQTT
protocol so that future message broker upgrades wont' be impacted.

..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
"""
import logging

from typing import Union, Optional, Callable

# Third-party library
import paho.mqtt.client as mqtt

from paho.mqtt.client import MQTTMessage

from pyshakealert.config import get_app_settings

settings = get_app_settings()


def default_on_message(topic: str, payload: str):
    logging.info(f'Received message: {payload}')
    logging.info(f'  Topic: {topic}')


class Client:
    """
    Client wrapper for stomp protocol used by ActiveMQ client
    """
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ca_certs: Optional[str] = None,
        keyfile: Optional[str] = None,
        reconnect: int = 0,
        keepalive: int = 60,
    ) -> None:
        """
        :param str host: host to connect (default: localhost)
        :param int port: port to connect (default: 1883)
        :param str username: optional username cred
        :param str password: optional password cred
        :param int reconnect: reconnect interval in seconds (default: 0 = none)
        :param int keepalive: maximum period in seconds allowed
            between communications (default: 6)
        """
        # Establish connection and set defaults
        self.host = host
        self.port = port
        self.keepalive = keepalive

        logging.info('Initiate MQTT client')
        self.client = mqtt.Client()
        self.client.enable_logger()
        if ca_certs is not None:
            self.client.tls_set(ca_certs=ca_certs, keyfile=keyfile)
            # TODO: our host is not in their certifi
            self.client.tls_insecure_set(True)
        if username is not None:
            logging.info(f'  credentials: {username}')
            self.client.username_pw_set(username, password=password)
        if reconnect:
            logging.info(f'  reconnect: {reconnect}')
            self.client.reconnect_delay_set(
                min_delay=reconnect,
                max_delay=reconnect)

    def disconnect(self) -> None:
        """
        Disconnect from the connection
        """
        self.client.disconnect()

    def subscribe(
        self,
        topic: str,
        on_message: Callable[[str, str], None] = default_on_message,
    ) -> None:
        """
        Subcribe to the topic sent and listen for messages

        A default listenery is set using MyDefaultListener which just outputs
        the content of the message to stdout.  The listener must follow
        the same template.

        ..  note::
            This routine is blocking.  Although we exit the routine, the
            thread is still running until the object is destroyed

        :param str topic: ActiveMQ topic to subcribe too
        :param callable on_message: on message hanlder with
            topic, payload as arg
        """
        def on_message_handler(client, userdata, message: MQTTMessage):
            logging.info(f'Received message on \
{message.topic}:\n{message.payload}')
            on_message(message.topic, message.payload.decode('utf-8'))
        self.client.on_message = on_message_handler

        # Subscribing in on_connect() means that if we lose the connection
        # and reconnect then subscriptions will be renewed.
        def on_connect_handler(client: mqtt.Client, userdata, flags, rc):
            logging.info(f'Subscribing to topic {topic}')
            client.subscribe(topic, 1)
        self.client.on_connect = on_connect_handler

        logging.info(f'Connecting to {self.host}:{self.port}')
        self.client.connect(
            self.host, self.port, keepalive=self.keepalive)
        self.client.loop_start()

    def publish(
        self,
        topic: str,
        body: Union[str, bytes],
    ) -> None:
        """
        Send a message to the ActiveMQ broker

        It is assumed that all message are in UTF-8

        :param str topic: topic to sent to
        :param str body: body content
        """
        if not self.client.is_connected():
            logging.info(f'Connecting to {self.host}:{self.port}')
            self.client.connect(
                self.host, self.port, keepalive=self.keepalive)

        logging.info(f'Sending message to broker topic {topic}')
        self.client.publish(
            topic,
            payload=body.encode('utf-8') if isinstance(body, str) else body,
        )

'''
Models
======

Model information

..  codeauthor:: Charles Blais
'''
from pyshakealert.message.event.event import Event


class Client:
    def send(self, event: Event) -> bool:
        raise NotImplementedError('send not defined for client')

'''
..  codeauthor:: Charles Blais
'''


class TankException(Exception):
    """Tankfile exception"""


class EmptyEventException(Exception):
    """Empty event exception"""


class ConnectFailedException(Exception):
    """Connection failed"""


class MissingCredentialsException(Exception):
    """Missing credentials"""

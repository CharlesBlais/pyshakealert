'''
..  codeauthor:: Charles Blais <charles.blais@nrcan-rncan.gc.ca>
'''
import logging
from enum import Enum
from typing import Optional

from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


class LogLevels(Enum):
    DEBUG: str = 'DEBUG'
    INFO: str = 'INFO'
    WARNING: str = 'WARNING'
    ERROR: str = 'ERROR'


class AppSettings(BaseSettings):
    log_level: LogLevels = LogLevels.WARNING
    log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
    log_datefmt: str = '%Y-%m-%d %H:%M:%S'

    # Email server settings
    email_from: str = 'cnsnopr@seismo.nrcan.gc.ca'
    smtp_server: str = 'mailhost.seismo.nrcan.gc.ca'

    # templates
    template_dir = str(Path(__file__).parent.joinpath('files', 'templates'))

    # shakealert
    dm_schema = str(Path(__file__).parent.joinpath(
        'files', 'schemas', 'ShakeAlert_Message_v10_20191004.xsd'))

    # earthworm
    ms2tank = '/app/eewdata/ew/bin/ms2tank'
    ms2tank_timeout = 10        # seconds
    ms2tank_pad_before = 60     # seconds
    ms2tank_pad_after = 600     # seconds
    ms2tank_buffer_size = 1     # seconds

    # activemq
    amq_host = 'localhost'
    amq_username: Optional[str] = None
    amq_password: Optional[str] = None
    amq_mqtt_port = 1883
    # amq_wp = 1884
    # amq_sa = 1893
    # amq_dm = 8883 (ssl)
    amq_stomp_port = 61613
    # amq_wp = 62613 (62612 - SSL)
    # amq_sa = 63613 (63612 - SSL)
    # amq_dm = 61613 (61612 - SSL)

    message_expires = 600   # seconds
    message_content_type = 'application/xml'

    # fdsnws
    fdsnws = 'http://fdsn.seismo.nrcan.gc.ca'

    # MMI color configuration, array per MMI level from 0
    mmi_colors = [
        '#ffffff',  # 0
        '#ffffff',  # 1
        '#b4c3fb',  # 2
        '#82effd',  # 3
        '#6ffffa',  # 4
        '#7bfc6c',  # 5
        '#ffff13',  # 6
        '#f2b11e',  # 7
        '#fd680a',  # 8
        '#f90003',  # 9
        '#be0006',  # 10
    ]

    class Config:
        env_file = '.env'
        env_prefix = 'shakealert_'

    @property
    def template_chanfile(self) -> Template:
        return Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True).get_template('chanfile_local.dat.j2')

    @property
    def template_mail(self) -> Template:
        return Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True).get_template('mail.html.j2')

    def configure_logging(self):
        '''
        Configure logging for app
        '''
        level = {
            LogLevels.DEBUG: logging.DEBUG,
            LogLevels.INFO: logging.INFO,
            LogLevels.WARNING: logging.WARNING,
            LogLevels.ERROR: logging.ERROR,
        }[self.log_level]
        logging.basicConfig(
            format=self.log_format,
            datefmt=self.log_datefmt,
            level=level)


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()

'''
..  codeauthor:: Charles Blais
'''
import logging
from enum import Enum

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

    # templates
    template_dir = str(Path(__file__).parent.joinpath('files', 'templates'))
    template_channel_file = 'chanfile_local.dat.j2'

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
    amq_username = ''
    amq_password = ''
    amq_port = 61613

    message_expires = 600   # seconds

    # fdsnws
    fdsnws = 'http://fdsn.seismo.nrcan.gc.ca'

    class Config:
        env_file = '.env'
        env_prefix = 'shakealert_'

    @property
    def template_chanfile(self) -> Template:
        return Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True).get_template(self.template_channel_file)

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

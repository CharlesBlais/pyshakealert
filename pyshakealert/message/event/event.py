"""
ShakeAlert Event
================

Object for handling ShakeAlert Event as described
in XML schema under schema/dm_message.xsd directory

..  note:: we know its validate before assignment

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

import datetime
from typing import Optional

from .core import Core
from .contributor import Contributors
from .gm import GroundMotion


@dataclass
class Event:
    class Meta:
        name = "event"
        nillable = True

    core_info: Core

    version: int = field(
        default=0,
        metadata=dict(type="Attribute"))

    orig_sys: str = field(
        default='dm',
        metadata=dict(type="Attribute"))

    message_type: str = field(
        default='new',
        metadata=dict(type="Attribute"))

    category: str = field(
        default='live',
        metadata=dict(type="Attribute"))

    timestamp: str = field(
        default=datetime.datetime.now().isoformat(),
        metadata=dict(type="Attribute"))

    alg_vers: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute"))

    instance: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute"))

    ref_id: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    ref_src: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute"))

    contributors: Optional[Contributors] = field(
        default=None)

    gm_info: Optional[GroundMotion] = field(
        default=None)

    fault_info: Optional[object] = field(
        default=None)

"""
ShakeAlert Event
================

Object for handling ShakeAlert Event as described
in XML schema under schema/dm_message.xsd directory

..  note:: we know its validate before assignment

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional

from .core_info import CoreInfo
from .contributors import Contributors
from .gm_info import GroundMotionInformation
from .follow_up_info import FollowUpInformation
from .fault_info import FaultInformation


@dataclass
class Event:
    class Meta:
        name = "event"
        nillable = True

    core_info: CoreInfo

    version: int = field(metadata=dict(type="Attribute"))

    orig_sys: str = field(metadata=dict(type="Attribute"))

    message_type: str = field(metadata=dict(type="Attribute"))

    contributors: Optional[Contributors] = field(default=None)

    fault_info: Optional[FaultInformation] = field(default=None)

    gm_info: Optional[GroundMotionInformation] = field(default=None)

    follow_up_info: Optional[FollowUpInformation] = field(default=None)

    category: str = field(default='live', metadata=dict(type="Attribute"))

    timestamp: str = field(default='-', metadata=dict(type="Attribute"))

    alg_vers: str = field(default='-', metadata=dict(type="Attribute"))

    instance: str = field(default='-', metadata=dict(type="Attribute"))

    ref_id: str = field(default='-', metadata=dict(type="Attribute"))

    ref_src: Optional[str] = field(
        default='-', metadata=dict(type="Attribute"))

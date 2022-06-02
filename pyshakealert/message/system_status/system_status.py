"""
ShakeAlert HA system
====================

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import List

from .component import Component


@dataclass
class SystemStatus:
    class Meta:
        name = "system_status"
        nillable = True

    alg_name: str = field(metadata=dict(type="Attribute"))

    alg_version: str = field(metadata=dict(type="Attribute"))

    count: int = field(metadata=dict(type="Attribute"))

    instance: str = field(metadata=dict(type="Attribute"))

    missing: int = field(metadata=dict(type="Attribute"))

    required: int = field(metadata=dict(type="Attribute"))

    status: str = field(metadata=dict(type="Attribute"))

    timestamp: str = field(metadata=dict(type="Attribute"))

    unexpected: int = field(metadata=dict(type="Attribute"))

    component: List[Component] = field(default_factory=list)

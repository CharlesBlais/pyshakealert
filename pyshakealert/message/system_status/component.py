"""
ShakeAlert HA component
=======================

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import List

from .subcomponent import SubComponent


@dataclass
class Component:
    count: int = field(metadata=dict(type="Attribute"))

    missing: int = field(metadata=dict(type="Attribute"))

    name: str = field(metadata=dict(type="Attribute"))

    required: int = field(metadata=dict(type="Attribute"))

    status: str = field(metadata=dict(type="Attribute"))

    subcomponent: List[SubComponent] = field(default_factory=list)

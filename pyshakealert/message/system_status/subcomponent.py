"""
ShakeAlert HA subcomponent
===========================

..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field


@dataclass
class SubComponent:
    name: str = field(metadata=dict(type="Attribute"))

    status: str = field(metadata=dict(type="Attribute"))

    timestamp: str = field(metadata=dict(type="Attribute"))

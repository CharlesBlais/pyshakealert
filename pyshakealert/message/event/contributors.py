"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import List


@dataclass
class Contributor:
    alg_instance: str = field(metadata=dict(type="Attribute"))

    alg_name: str = field(metadata=dict(type="Attribute"))

    alg_version: str = field(metadata=dict(type="Attribute"))

    category: str = field(metadata=dict(type="Attribute"))

    event_id: str = field(metadata=dict(type="Attribute"))

    version: int = field(metadata=dict(type="Attribute"))


@dataclass
class Contributors:
    contributor: List[Contributor] = field(
        default_factory=list)

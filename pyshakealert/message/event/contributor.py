"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Contributor:
    alg_name: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    alg_version: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    alg_instance: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    category: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    event_id: str = field(
        default='-',
        metadata=dict(type="Attribute"))

    version: int = field(
        default=0,
        metadata=dict(type="Attribute"))


@dataclass
class Contributors:
    contributor: List[Contributor] = field(
        default_factory=list)

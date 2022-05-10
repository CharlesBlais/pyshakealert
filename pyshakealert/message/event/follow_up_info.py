"""
..  codeauthor:: Charles Blais
"""
from dataclasses import dataclass, field

from typing import Optional


@dataclass
class FollowUpInformation:
    message_text: Optional[str] = field(
        default=None,
        metadata=dict(type="Attribute"))

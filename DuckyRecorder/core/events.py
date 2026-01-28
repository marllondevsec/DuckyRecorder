from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class EventType(Enum):
    TEXT = auto()
    KEY = auto()
    MOUSE_MOVE = auto()
    MOUSE_CLICK = auto()
    MOUSE_ZERO = auto()


@dataclass
class Event:
    type: EventType
    data: dict
    timestamp: Optional[float] = field(default=None)

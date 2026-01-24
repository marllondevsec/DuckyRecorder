from dataclasses import dataclass
from enum import Enum, auto


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

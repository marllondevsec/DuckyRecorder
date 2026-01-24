from .ducky import export_to_ducky
from .arduino import export_to_arduino

EXPORTERS = {
    "ducky": {
        "label": "Rubber Ducky (.txt)",
        "ext": ".ducky.txt",
        "func": export_to_ducky,
    },
    "arduino": {
        "label": "Arduino HID (.ino)",
        "ext": ".ino",
        "func": export_to_arduino,
    },
}


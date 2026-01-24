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
        "func": lambda input_path, output_path: export_to_arduino(input_path, output_path, fast_mode=True, zero_mouse=True),
    },
}

__all__ = ['export_to_ducky', 'export_to_arduino', 'EXPORTERS']

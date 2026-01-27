"""Mapeamento de teclas de atalho"""

from pynput.keyboard import Key

# Mapeamento de string para objeto Key
KEY_MAP = {
    'F1': Key.f1,
    'F2': Key.f2,
    'F3': Key.f3,
    'F4': Key.f4,
    'F5': Key.f5,
    'F6': Key.f6,
    'F7': Key.f7,
    'F8': Key.f8,
    'F9': Key.f9,
    'F10': Key.f10,
    'F11': Key.f11,
    'F12': Key.f12,
    'ESC': Key.esc,
    'PAUSE': Key.pause,
    'PRINT_SCREEN': Key.print_screen,
    'SCROLL_LOCK': Key.scroll_lock,
}

def get_key_from_string(key_string):
    """Converte string para objeto Key"""
    return KEY_MAP.get(key_string.upper(), Key.f9)  # Default F9

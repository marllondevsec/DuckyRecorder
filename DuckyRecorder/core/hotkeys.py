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
    'INSERT': Key.insert,
    'DELETE': Key.delete,
    'HOME': Key.home,
    'END': Key.end,
    'PAGE_UP': Key.page_up,
    'PAGE_DOWN': Key.page_down,
    'CAPS_LOCK': Key.caps_lock,
    'NUM_LOCK': Key.num_lock,
    'ENTER': Key.enter,
    'SPACE': Key.space,
    'TAB': Key.tab,
    'BACKSPACE': Key.backspace,
    'SHIFT': Key.shift,
    'CTRL': Key.ctrl,
    'ALT': Key.alt,
    'CMD': Key.cmd,
    'UP': Key.up,
    'DOWN': Key.down,
    'LEFT': Key.left,
    'RIGHT': Key.right,
}

def get_key_from_string(key_string):
    """Converte string para objeto Key"""
    return KEY_MAP.get(key_string.upper(), Key.f9)  # Default F9

def get_available_keys():
    """Retorna lista de teclas disponíveis para configuração"""
    return list(KEY_MAP.keys())

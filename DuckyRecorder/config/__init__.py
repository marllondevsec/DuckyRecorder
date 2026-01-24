import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
RECORDINGS_DIR = BASE_DIR / "recordings"
LANG_DIR = BASE_DIR / "DuckyRecorder" / "lang"

# Configurações
SETTINGS = {
    "default_language": "pt",
    "mouse_speed": "FAST",  # FAST, MEDIUM, SLOW
    "zero_mouse_on_start": True,
    "auto_save": True,
}

def ensure_directories():
    """Garante que os diretórios necessários existam"""
    RECORDINGS_DIR.mkdir(exist_ok=True)
    (BASE_DIR / "exports").mkdir(exist_ok=True)

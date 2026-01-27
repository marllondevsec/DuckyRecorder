import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
RECORDINGS_DIR = BASE_DIR / "recordings"
LANG_DIR = BASE_DIR / "DuckyRecorder" / "lang"
CONFIG_FILE = BASE_DIR / "config.json"

# Configurações padrão
SETTINGS = {
    "language": "pt",
    "mouse_speed": "FAST",  # FAST, MEDIUM, SLOW
    "zero_mouse_on_start": True,
    "auto_save": True,
    "pause_key": "F9",
    "stop_key": "F10",
    "default_recording_name": "",
    "show_live_preview": True,
    "max_events_display": 10
}

def ensure_directories():
    """Garante que os diretórios necessários existam"""
    RECORDINGS_DIR.mkdir(exist_ok=True)
    (BASE_DIR / "exports").mkdir(exist_ok=True)

def load_config():
    """Carrega a configuração do arquivo ou retorna padrão"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge com configurações padrão para garantir todas as chaves existem
                for key, value in SETTINGS.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception:
            return SETTINGS.copy()
    else:
        return SETTINGS.copy()

def save_config(config):
    """Salva a configuração no arquivo"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_language():
    """Retorna o idioma atual da configuração"""
    config = load_config()
    return config.get("language", "pt")

def update_config(key, value):
    """Atualiza uma configuração específica"""
    config = load_config()
    config[key] = value
    save_config(config)
    return config

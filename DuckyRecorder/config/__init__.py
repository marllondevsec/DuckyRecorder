import os
import json
from pathlib import Path

# Caminho absoluto para o diretório raiz do projeto
# __file__ = /home/ghostkernel/Documents/GitHub/DuckyRecorder/DuckyRecorder/config/__init__.py
# parent.parent.parent = /home/ghostkernel/Documents/GitHub/DuckyRecorder
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Vai até DuckyRecorder/
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "config.json"

print(f"DEBUG: PROJECT_ROOT = {PROJECT_ROOT}")
print(f"DEBUG: CONFIG_FILE = {CONFIG_FILE}")
print(f"DEBUG: CONFIG_FILE existe? {CONFIG_FILE.exists()}")

# Garante que o diretório config existe
CONFIG_DIR.mkdir(exist_ok=True)

# Configurações padrão
SETTINGS = {
    "language": "pt",
    "mouse_speed": "FAST",
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
    CONFIG_DIR.mkdir(exist_ok=True)
    recordings_dir = PROJECT_ROOT / "recordings"
    exports_dir = PROJECT_ROOT / "exports"
    recordings_dir.mkdir(exist_ok=True)
    exports_dir.mkdir(exist_ok=True)
    print(f"DEBUG: Diretórios criados/verificados em {PROJECT_ROOT}")

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
                print(f"DEBUG: Config carregada de {CONFIG_FILE}")
                return config
        except Exception as e:
            print(f"⚠️  Erro ao carregar config.json: {e}")
            # Se houver erro, salva configuração padrão
            save_config(SETTINGS.copy())
            return SETTINGS.copy()
    else:
        # Se não existir, cria com configurações padrão
        print(f"DEBUG: Criando config padrão em {CONFIG_FILE}")
        save_config(SETTINGS.copy())
        return SETTINGS.copy()

def save_config(config):
    """Salva a configuração no arquivo"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"DEBUG: Config salva em {CONFIG_FILE}")
    except Exception as e:
        print(f"⚠️  Erro ao salvar config.json: {e}")

def get_language():
    """Retorna o idioma atual da configuração"""
    config = load_config()
    lang = config.get("language", "pt")
    print(f"DEBUG: get_language() retornando: {lang}")
    return lang

def update_config(key, value):
    """Atualiza uma configuração específica"""
    config = load_config()
    config[key] = value
    save_config(config)
    return config

from DuckyRecorder.core.colors import green, red, yellow, cyan
from DuckyRecorder.utils.console import clear
from DuckyRecorder.core.recorder import Recorder
from DuckyRecorder.exporters import EXPORTERS
from DuckyRecorder.core.language import t, set_language, get_current_language
from DuckyRecorder.config import load_config, save_config, update_config
# CORREÇÃO: Importar corretamente do pacote raiz
import sys
import os

# Adiciona o diretório pai ao sys.path para acessar o módulo raiz
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from DuckyRecorder import show_banner

import time
import json
from pathlib import Path


# Caminhos corrigidos
BASE_DIR = Path(__file__).parent.parent.parent  # DuckyRecorder/
PROJECT_ROOT = BASE_DIR.parent  # Diretório do projeto
RECORDINGS_DIR = PROJECT_ROOT / "recordings"
EXPORTS_DIR = PROJECT_ROOT / "exports"


def main_menu():
    # Garante que os diretórios existam
    RECORDINGS_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    
    while True:
        clear()
        # Agora a importação funcionará
        show_banner()
        print()  # Linha em branco para separar
        
        print(green("1) " + t("menu_start")))
        print(green("2) " + t("menu_list")))
        print(green("3) " + t("menu_export")))
        print(green("4) " + t("menu_settings")))
        print(red("0) " + t("menu_exit") + "\n"))
        
        choice = input(yellow(t("choose_option") + ": ")).strip()
        
        if choice == "1":
            start_recording()
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            export_recording()
        elif choice == "4":
            settings_menu()
        elif choice == "0":
            clear()
            print(red(t("exiting")))
            break
        else:
            input(red(t("invalid_option")))

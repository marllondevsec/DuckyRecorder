from DuckyRecorder.core.colors import green, red, yellow, cyan
from DuckyRecorder.utils.console import clear
from DuckyRecorder.core.recorder import Recorder
from DuckyRecorder.exporters import EXPORTERS
from DuckyRecorder.core.language import t, set_language, get_current_language
from DuckyRecorder.config import load_config, save_config, update_config, CONFIG_FILE
from DuckyRecorder.core.hotkeys import get_available_keys
from DuckyRecorder.utils.logger import debug, info, warning, error, logger
import sys
import os

# Adiciona o diretório pai ao sys.path para acessar o módulo raiz
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from DuckyRecorder import show_banner

import time
import json
from pathlib import Path
from datetime import datetime


# CORREÇÃO: Caminhos absolutos para o projeto
# __file__ = /home/ghostkernel/Documents/GitHub/DuckyRecorder/DuckyRecorder/cli/menu.py
# parent.parent.parent = /home/ghostkernel/Documents/GitHub/DuckyRecorder
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Vai até DuckyRecorder/
RECORDINGS_DIR = PROJECT_ROOT / "recordings"
EXPORTS_DIR = PROJECT_ROOT / "exports"

debug(f"PROJECT_ROOT = {PROJECT_ROOT}")
debug(f"RECORDINGS_DIR = {RECORDINGS_DIR}")
debug(f"EXPORTS_DIR = {EXPORTS_DIR}")


def _ensure_dirs():
    RECORDINGS_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    debug(f"Diretórios garantidos:")
    debug(f"  - {RECORDINGS_DIR}")
    debug(f"  - {EXPORTS_DIR}")


def _choose_from_list(items, prompt):
    """
    Mostra lista numerada e retorna índice (0-based) ou None se cancelado.
    """
    if not items:
        print(red(t("no_recordings")))
        input(yellow(t("enter_return")))
        return None

    for i, name in enumerate(items, start=1):
        print(f"{i}) {name}")
    print("0) " + t("menu_exit"))

    while True:
        choice = input(yellow(prompt + ": ")).strip()
        if choice == "0":
            return None
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(items):
                return idx - 1
        print(red(t("invalid_option")))


def start_recording():
    """
    Inicia o Recorder, aguarda até o usuário parar (tecla configurada),
    salva a gravação em recordings/ e notifica.
    """
    config = load_config()
    recorder = Recorder(config=config)

    # Pergunta por nome opcional
    name = input(yellow("Nome da gravação (ENTER para gerar com timestamp): ")).strip()
    if not name:
        name = datetime.now().strftime("rec_%Y%m%d_%H%M%S")
    filename = f"{name}.json"
    out_path = RECORDINGS_DIR / filename

    # Inicia gravação
    clear()
    show_banner()
    print()
    print(green(f"🎙️  {t('recording_started')}"))
    recorder.start(recording_name=name)

    # Aguarda até recorder.is_recording virar False (usuário pressionou stop_key)
    try:
        while recorder.is_recording:
            time.sleep(0.2)
    except KeyboardInterrupt:
        # Se for interrompido pelo teclado, tenta parar limpamente
        recorder.stop()

    # Garante que listeners foram parados e salva
    recorder.stop()
    recorder.save(str(out_path))

    print(green(f"{t('recording_saved')} {out_path}"))
    input(yellow(t("enter_return")))


def list_recordings():
    """Lista gravações disponíveis e mostra informações básicas."""
    _ensure_dirs()
    files = sorted([f.name for f in RECORDINGS_DIR.glob("*.json")])
    clear()
    show_banner()
    print()
    if not files:
        print(red(t("no_recordings")))
        input(yellow(t("enter_return")))
        return

    print(green(t("recordings_available")))
    for i, f in enumerate(files, start=1):
        print(f"  {i}) {f}")
    print()
    input(yellow(t("enter_return")))


def export_recording():
    """Exporta uma gravação para um formato disponível em EXPORTERS."""
    _ensure_dirs()
    files = sorted([f.name for f in RECORDINGS_DIR.glob("*.json")])
    clear()
    show_banner()
    print()

    idx = _choose_from_list(files, t("select_recording"))
    if idx is None:
        return

    input_file = RECORDINGS_DIR / files[idx]

    # Escolhe exportador
    exporter_keys = list(EXPORTERS.keys())
    print()
    for i, key in enumerate(exporter_keys, start=1):
        label = EXPORTERS[key].get("label", key)
        print(f"{i}) {label}")
    print("0) " + t("enter_return"))

    while True:
        choice = input(yellow(t("select_export") + ": ")).strip()
        if choice == "0":
            return
        if choice.isdigit():
            xi = int(choice)
            if 1 <= xi <= len(exporter_keys):
                exporter_key = exporter_keys[xi - 1]
                exporter = EXPORTERS[exporter_key]
                break
        print(red(t("invalid_option")))

    out_name = input(yellow("Nome do arquivo de saída (sem extensão, ENTER = nome da gravação): ")).strip()
    if not out_name:
        out_name = input_file.stem
    out_path = EXPORTS_DIR / (out_name + exporter["ext"])

    # Executa export
    try:
        func = exporter["func"]
        result = func(str(input_file), str(out_path))
        print(green(f"{t('export_success')} {out_path}"))
    except Exception as e:
        print(red(f"Erro ao exportar: {e}"))
    input(yellow(t("enter_return")))


def settings_menu():
    """Menu de configurações completo com todas as opções."""
    config = load_config()
    while True:
        clear()
        show_banner()
        print()
        print(cyan(f"📁 Configurações | Arquivo: {CONFIG_FILE}"))
        print()
        print(green("1) ") + t("select_lang"))
        print(green("2) Mostrar pré-visualização ao vivo: ") + (green("ON") if config.get("show_live_preview", True) else red("OFF")))
        print(green(f"3) Tecla para pausar: {config.get('pause_key', 'F9')}"))
        print(green(f"4) Tecla para parar: {config.get('stop_key', 'F10')}"))
        print(green("5) Velocidade do mouse: ") + config.get('mouse_speed', 'FAST'))
        print(green("6) Zerar mouse no início: ") + (green("ON") if config.get('zero_mouse_on_start', True) else red("OFF")))
        print(red("0) " + t("enter_return")))
        choice = input(yellow(t("choose_option") + ": ")).strip()

        if choice == "1":
            # CORREÇÃO: Usar o caminho correto para o diretório lang
            lang_dir = Path(__file__).parent.parent / "lang"
            info(f"Procurando idiomas em: {lang_dir}")
            
            if not lang_dir.exists():
                print(red(f"Diretório não encontrado: {lang_dir}"))
                input(yellow(t("enter_return")))
                continue
                
            langs = []
            for p in sorted(lang_dir.glob("*.json")):
                langs.append(p.stem)
            
            if not langs:
                print(red("Nenhum arquivo de idioma encontrado"))
                print(yellow(f"Procurando em: {lang_dir}"))
                input(yellow(t("enter_return")))
                continue
                
            print(cyan("Idiomas disponíveis:"))
            for i, l in enumerate(langs, start=1):
                print(f"{i}) {l}")
            print("0) " + t("enter_return"))
            
            sel = input(yellow(t("select_lang") + ": ")).strip()
            if sel == "0":
                continue
            if sel.isdigit():
                si = int(sel)
                if 1 <= si <= len(langs):
                    new_lang = langs[si - 1]
                    update_config("language", new_lang)
                    set_language(new_lang)
                    config = load_config()
                    print(green(t("lang_set").format(new_lang)))
                    input(yellow(t("enter_return")))
                    continue
            print(red(t("invalid_option")))
            input(yellow(t("enter_return")))

        elif choice == "2":
            # Toggle show_live_preview
            new_val = not config.get("show_live_preview", True)
            update_config("show_live_preview", new_val)
            config = load_config()
            state = "ON" if new_val else "OFF"
            info(f"show_live_preview: {state}")
            print(green(f"show_live_preview: {state}"))
            input(yellow(t("enter_return")))

        elif choice == "3":
            # Configurar tecla de pausa
            available_keys = get_available_keys()
            print("\n" + cyan("Teclas disponíveis:"))
            for i, key in enumerate(available_keys, 1):
                print(f"  {i:2}) {key}")
            print("  0) Cancelar")
            
            try:
                sel = input(yellow("Selecione o número da tecla para pausa: ")).strip()
                if sel == "0":
                    continue
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(available_keys):
                        new_key = available_keys[idx]
                        update_config("pause_key", new_key)
                        config = load_config()
                        info(f"Tecla de pausa definida como: {new_key}")
                        print(green(f"Tecla de pausa definida como: {new_key}"))
                        input(yellow(t("enter_return")))
                        continue
                print(red("Seleção inválida!"))
            except Exception as e:
                error(f"Erro: {e}")
                print(red(f"Erro: {e}"))
            input(yellow(t("enter_return")))

        elif choice == "4":
            # Configurar tecla de parada
            available_keys = get_available_keys()
            print("\n" + cyan("Teclas disponíveis:"))
            for i, key in enumerate(available_keys, 1):
                print(f"  {i:2}) {key}")
            print("  0) Cancelar")
            
            try:
                sel = input(yellow("Selecione o número da tecla para parar: ")).strip()
                if sel == "0":
                    continue
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(available_keys):
                        new_key = available_keys[idx]
                        update_config("stop_key", new_key)
                        config = load_config()
                        info(f"Tecla de parada definida como: {new_key}")
                        print(green(f"Tecla de parada definida como: {new_key}"))
                        input(yellow(t("enter_return")))
                        continue
                print(red("Seleção inválida!"))
            except Exception as e:
                error(f"Erro: {e}")
                print(red(f"Erro: {e}"))
            input(yellow(t("enter_return")))

        elif choice == "5":
            # Configurar velocidade do mouse
            speeds = ["FAST", "MEDIUM", "SLOW"]
            print("\n" + cyan("Velocidades disponíveis:"))
            for i, speed in enumerate(speeds, 1):
                print(f"  {i}) {speed}")
            print("  0) Cancelar")
            
            sel = input(yellow("Selecione a velocidade do mouse: ")).strip()
            if sel == "0":
                continue
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(speeds):
                    update_config("mouse_speed", speeds[idx])
                    config = load_config()
                    info(f"Velocidade do mouse definida como: {speeds[idx]}")
                    print(green(f"Velocidade do mouse definida como: {speeds[idx]}"))
                    input(yellow(t("enter_return")))
                    continue
            print(red("Seleção inválida!"))
            input(yellow(t("enter_return")))

        elif choice == "6":
            # Toggle zero_mouse_on_start
            new_val = not config.get('zero_mouse_on_start', True)
            update_config('zero_mouse_on_start', new_val)
            config = load_config()
            state = "ON" if new_val else "OFF"
            info(f"Zerar mouse no início: {state}")
            print(green(f"Zerar mouse no início: {state}"))
            input(yellow(t("enter_return")))

        elif choice == "0":
            break

        else:
            input(red(t("invalid_option")))


def show_debug_logs():
    """Exibe os logs de debug em um submenu"""
    while True:
        clear()
        show_banner()
        print()
        print(cyan("📋 LOGS DE DEBUG"))
        print()
        
        messages = logger.get_messages(20)  # Últimas 20 mensagens
        if not messages:
            print(yellow("Nenhuma mensagem de debug disponível."))
        else:
            for i, msg in enumerate(messages, 1):
                # Remove o timestamp para visualização mais limpa
                if "DEBUG]" in msg:
                    # Mensagens DEBUG em cinza
                    print(f"\033[90m{i:2}) {msg[15:]}\033[0m")
                elif "INFO]" in msg:
                    # Mensagens INFO em azul
                    print(f"\033[94m{i:2}) {msg[15:]}\033[0m")
                elif "WARNING]" in msg:
                    # Mensagens WARNING em amarelo
                    print(f"\033[93m{i:2}) {msg[15:]}\033[0m")
                elif "ERROR]" in msg:
                    # Mensagens ERROR em vermelho
                    print(f"\033[91m{i:2}) {msg[15:]}\033[0m")
                else:
                    print(f"{i:2}) {msg[15:]}")
        
        print()
        print(green("1) Atualizar logs"))
        print(green("2) Limpar logs"))
        print(green("3) Mostrar todos os logs (últimos 100)"))
        print(green("4) Exportar logs para arquivo"))
        print(red("0) Voltar"))
        
        choice = input(yellow("Escolha uma opção: ")).strip()
        
        if choice == "1":
            continue  # Apenas atualiza a tela
        elif choice == "2":
            logger.clear()
            print(green("Logs limpos com sucesso!"))
            input(yellow("ENTER para continuar..."))
        elif choice == "3":
            messages = logger.get_messages(100)
            clear()
            print(cyan("📋 TODOS OS LOGS (ÚLTIMOS 100)"))
            print("-" * 80)
            for msg in messages:
                print(msg)
            print("-" * 80)
            input(yellow("\nENTER para voltar..."))
        elif choice == "4":
            if logger.log_file and logger.log_file.exists():
                print(green(f"Logs exportados para: {logger.log_file}"))
                print(yellow(f"Total de mensagens: {len(logger.messages)}"))
            else:
                print(red("Arquivo de log não encontrado!"))
            input(yellow("ENTER para continuar..."))
        elif choice == "0":
            break
        else:
            input(red("Opção inválida!"))


def main_menu():
    # Garante que os diretórios existam
    _ensure_dirs()

    while True:
        clear()
        show_banner()
        print()

        print(green("1) " + t("menu_start")))
        print(green("2) " + t("menu_list")))
        print(green("3) " + t("menu_export")))
        print(green("4) " + t("menu_settings")))
        print(green("5) 📋 Logs de debug"))
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
        elif choice == "5":  # NOVA OPÇÃO
            show_debug_logs()
        elif choice == "0":
            clear()
            print(red(t("exiting")))
            break
        else:
            input(red(t("invalid_option")))

# Adicionar exportação da função main_menu
__all__ = ['main_menu']

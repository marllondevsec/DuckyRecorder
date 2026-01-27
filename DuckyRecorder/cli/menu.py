from DuckyRecorder.core.colors import green, red, yellow, cyan
from DuckyRecorder.utils.console import clear
from DuckyRecorder.core.recorder import Recorder
from DuckyRecorder.exporters import EXPORTERS
from DuckyRecorder.core.language import t, set_language, get_current_language
from DuckyRecorder.config import load_config, save_config, update_config

import time
import os
import json


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")


def main_menu():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    while True:
        clear()
        print(cyan("╔══════════════════════════════╗"))
        print(cyan("║    " + t("app_title").center(20) + "    ║"))
        print(cyan("╚══════════════════════════════╝\n"))

        print(green("1) " + t("menu_start")))
        print(green("2) " + t("menu_list")))
        print(green("3) " + t("menu_export")))
        print(green("4) " + t("menu_settings")))  # Mudado de menu_lang para menu_settings
        print(red("0) " + t("menu_exit") + "\n"))

        choice = input(yellow(t("choose_option") + ": ")).strip()

        if choice == "1":
            start_recording()
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            export_recording()
        elif choice == "4":
            settings_menu()  # Novo menu de configurações
        elif choice == "0":
            clear()
            print(red(t("exiting")))
            break
        else:
            input(red(t("invalid_option")))


# --------------------------------------------------

def start_recording():
    clear()
    config = load_config()
    
    # Pergunta nome para a gravação
    default_name = config.get("default_recording_name", "")
    if default_name:
        prompt = f"Nome da gravação [{default_name}]: "
    else:
        prompt = "Nome da gravação (deixe em branco para usar data/hora): "
    
    recording_name = input(yellow(prompt)).strip()
    
    if not recording_name and default_name:
        recording_name = default_name
    elif not recording_name:
        recording_name = f"gravação_{time.strftime('%Y%m%d_%H%M%S')}"
    
    recorder = Recorder(config)

    print(green(t("recording_started")))
    print(yellow("\nControles:"))
    print(yellow("  F9: Pausar/Continuar"))
    print(yellow("  F10: Parar e salvar"))
    print(yellow("\nPressione F10 para finalizar a gravação...\n"))

    recorder.start(recording_name)
    
    # Aguarda o recorder terminar (será controlado por F10)
    while recorder.is_recording:
        time.sleep(0.1)
    
    # Quando F10 for pressionado, salva a gravação
    filename = f"{recording_name.replace(' ', '_')}_{int(time.time())}.json"
    path = os.path.join(RECORDINGS_DIR, filename)
    recorder.save(path)

    print(green(f"\n✓ {t('recording_saved')}"))
    print(yellow(f"  Arquivo: {filename}"))
    print(yellow(f"  Eventos: {recorder.event_count}"))
    input(yellow("\n" + t("enter_return")))


# --------------------------------------------------

def list_recordings():
    clear()
    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".json")]

    if not files:
        print(red(t("no_recordings")))
    else:
        print(green(t("recordings_available") + ":\n"))
        for f in files:
            filepath = os.path.join(RECORDINGS_DIR, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    name = data.get('metadata', {}).get('name', f)
                    event_count = data.get('metadata', {}).get('event_count', 0)
                    duration = data.get('metadata', {}).get('duration', 0)
                    print(f" 📁 {name}")
                    print(f"    Eventos: {event_count} | Duração: {duration:.1f}s")
                    print(f"    Arquivo: {f}\n")
            except:
                print(f" - {f}")

    input(yellow("\n" + t("enter_return")))


# --------------------------------------------------

def export_recording():
    clear()
    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".json")]

    if not files:
        print(red(t("no_recordings")))
        input(yellow("\n" + t("enter_return")))
        return

    print(green(t("select_recording") + ":\n"))
    for i, f in enumerate(files):
        print(f"{i + 1}) {f}")

    try:
        choice = int(input(yellow("\n" + t("choose_option") + ": "))) - 1
        selected = files[choice]
    except (ValueError, IndexError):
        input(red(t("invalid_selection")))
        return

    input_path = os.path.join(RECORDINGS_DIR, selected)

    # -------- escolher exporter --------
    clear()
    print(green(t("select_export") + ":\n"))

    exporter_keys = list(EXPORTERS.keys())
    for i, key in enumerate(exporter_keys):
        print(f"{i + 1}) {EXPORTERS[key]['label']}")

    try:
        choice = int(input(yellow("\n" + t("choose_option") + ": "))) - 1
        exporter_key = exporter_keys[choice]
        exporter = EXPORTERS[exporter_key]
    except (ValueError, IndexError):
        input(red(t("invalid_selection")))
        return

    # helper local simples para perguntas sim/não com default
    def ask_bool(prompt: str, default: bool) -> bool:
        hint = "Y/n" if default else "y/N"
        resp = input(yellow(f"{prompt} [{hint}]: ")).strip().lower()
        if resp == "":
            return default
        return resp[0] in ("y", "s")  # aceita 'y' (yes) e 's' (sim)

    # Se o exporter for o Arduino, pergunta opções (zero_mouse e fast_mode)
    if exporter_key == "arduino":
        # importa aqui para poder usar a função com parâmetros
        from DuckyRecorder.exporters.arduino import export_to_arduino

        # lê defaults da config
        cfg = load_config()
        default_zero = cfg.get("zero_mouse_on_start", True)
        default_fast = (cfg.get("mouse_speed", "FAST").upper() == "FAST")

        clear()
        print(green("Configuração de exportação para Arduino:\n"))
        zero_mouse = ask_bool("Zerar mouse no início?", default_zero)
        fast_mode = ask_bool("Modo rápido (fast)?", default_fast)

        output_path = input_path.replace(".json", ".ino")
        export_to_arduino(input_path, output_path, fast_mode=fast_mode, zero_mouse=zero_mouse)

    else:
        # exportadores que não precisam de opções adicionais
        output_path = input_path.replace(".json", exporter["ext"])
        exporter["func"](input_path, output_path)

    print(green("\n" + t("export_success")))
    print(yellow(output_path))
    input(yellow("\n" + t("enter_return")))


# --------------------------------------------------

def settings_menu():
    """Menu de configurações"""
    while True:
        clear()
        config = load_config()
        
        print(cyan("╔══════════════════════════════╗"))
        print(cyan("║       CONFIGURAÇÕES          ║"))
        print(cyan("╚══════════════════════════════╝\n"))
        
        print(green("1) Idioma"))
        print(f"   Atual: {config.get('language', 'pt').upper()}")
        
        print(green("\n2) Teclas de atalho"))
        print(f"   Pausar/Continuar: {config.get('pause_key', 'F9')}")
        print(f"   Parar: {config.get('stop_key', 'F10')}")
        
        print(green("\n3) Configurações de gravação"))
        print(f"   Nome padrão: {config.get('default_recording_name', '(nenhum)')}")
        print(f"   Mostrar preview: {'Sim' if config.get('show_live_preview', True) else 'Não'}")
        
        print(green("\n4) Configurações de mouse"))
        print(f"   Velocidade: {config.get('mouse_speed', 'FAST')}")
        print(f"   Zerar mouse no início: {'Sim' if config.get('zero_mouse_on_start', True) else 'Não'}")
        
        print(red("\n0) Voltar ao menu principal\n"))
        
        choice = input(yellow("Escolha uma opção: ")).strip()
        
        if choice == "1":
            change_language()
        elif choice == "2":
            configure_hotkeys()
        elif choice == "3":
            configure_recording()
        elif choice == "4":
            configure_mouse()
        elif choice == "0":
            break
        else:
            input(red("Opção inválida. ENTER para continuar"))


def change_language():
    """Altera o idioma"""
    clear()
    print(green("Selecionar idioma:\n"))
    print("1) Português")
    print("2) English")
    
    choice = input(yellow("\nEscolha: ")).strip()
    
    if choice == "1":
        new_lang = "pt"
    elif choice == "2":
        new_lang = "en"
    else:
        input(red("Opção inválida"))
        return
    
    # Atualizar configuração
    update_config("language", new_lang)
    
    # Atualizar idioma no sistema
    set_language(new_lang)
    
    print(green(f"\nIdioma alterado para: {new_lang.upper()}"))
    input(yellow("\nENTER para continuar"))


def configure_hotkeys():
    """Configura as teclas de atalho"""
    clear()
    config = load_config()
    
    print(green("Configurar teclas de atalho:\n"))
    
    print("Teclas disponíveis: F1-F12, ESC, PAUSE, PRINT_SCREEN")
    
    current_pause = config.get('pause_key', 'F9')
    current_stop = config.get('stop_key', 'F10')
    
    new_pause = input(f"\nTecla para Pausar/Continuar [{current_pause}]: ").strip().upper()
    new_stop = input(f"Tecla para Parar [{current_stop}]: ").strip().upper()
    
    if new_pause:
        update_config('pause_key', new_pause)
    if new_stop:
        update_config('stop_key', new_stop)
    
    print(green("\nTeclas de atalho atualizadas!"))
    input(yellow("\nENTER para continuar"))


def configure_recording():
    """Configura opções de gravação"""
    clear()
    config = load_config()
    
    print(green("Configurações de gravação:\n"))
    
    current_name = config.get('default_recording_name', '')
    current_preview = config.get('show_live_preview', True)
    
    new_name = input(f"Nome padrão para gravações [{current_name}]: ").strip()
    preview_choice = input(f"Mostrar preview em tempo real? (S/N) [{'S' if current_preview else 'N'}]: ").strip().lower()
    
    if new_name != "":
        update_config('default_recording_name', new_name)
    
    if preview_choice in ['s', 'n']:
        update_config('show_live_preview', preview_choice == 's')
    
    print(green("\nConfigurações salvas!"))
    input(yellow("\nENTER para continuar"))


def configure_mouse():
    """Configura opções do mouse"""
    clear()
    config = load_config()
    
    print(green("Configurações do mouse:\n"))
    
    current_speed = config.get('mouse_speed', 'FAST')
    current_zero = config.get('zero_mouse_on_start', True)
    
    print("Velocidades disponíveis: FAST, MEDIUM, SLOW")
    new_speed = input(f"\nVelocidade do mouse [{current_speed}]: ").strip().upper()
    
    zero_choice = input(f"Zerar mouse no início? (S/N) [{'S' if current_zero else 'N'}]: ").strip().lower()
    
    if new_speed in ['FAST', 'MEDIUM', 'SLOW']:
        update_config('mouse_speed', new_speed)
    
    if zero_choice in ['s', 'n']:
        update_config('zero_mouse_on_start', zero_choice == 's')
    
    print(green("\nConfigurações do mouse atualizadas!"))
    input(yellow("\nENTER para continuar"))

from DuckyRecorder.core.colors import green, red, yellow, cyan
from DuckyRecorder.utils.console import clear
from DuckyRecorder.core.recorder import Recorder
from DuckyRecorder.exporters import EXPORTERS
from DuckyRecorder.core.language import t, set_language, get_current_language
from DuckyRecorder.config import load_config, save_config

import time
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")

def main_menu():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    while True:
        clear()
        print(cyan("╔════════════════════════╗"))
        print(cyan("║    " + t("app_title").center(16) + "    ║"))
        print(cyan("╚════════════════════════╝\n"))

        print(green("1) " + t("menu_start")))
        print(green("2) " + t("menu_list")))
        print(green("3) " + t("menu_export")))
        print(green("4) " + t("menu_lang")))
        print(red("0) " + t("menu_exit") + "\n"))

        choice = input(yellow(t("choose_option") + ": ")).strip()

        if choice == "1":
            start_recording()
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            export_recording()
        elif choice == "4":
            change_language()
        elif choice == "0":
            clear()
            print(red(t("exiting")))
            break
        else:
            input(red(t("invalid_option")))


# --------------------------------------------------

def start_recording():
    clear()
    recorder = Recorder()

    print(green(t("recording_started")))
    print(yellow(t("press_enter_stop") + "\n"))

    recorder.start()
    input()
    recorder.stop()

    filename = f"recording_{int(time.time())}.json"
    path = os.path.join(RECORDINGS_DIR, filename)
    recorder.save(path)

    print(green(f"\n{t('recording_saved')} {path}"))
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
        exporter = EXPORTERS[exporter_keys[choice]]
    except (ValueError, IndexError):
        input(red(t("invalid_selection")))
        return

    output_path = input_path.replace(".json", exporter["ext"])
    exporter["func"](input_path, output_path)

    print(green("\n" + t("export_success")))
    print(yellow(output_path))
    input(yellow("\n" + t("enter_return")))


# --------------------------------------------------

def change_language():
    clear()
    print(green(t("select_lang") + "\n"))
    print("1) " + t("lang_portuguese"))
    print("2) " + t("lang_english"))
    
    choice = input(yellow("\n" + t("choose_option") + ": ")).strip()
    
    if choice == "1":
        new_lang = "pt"
    elif choice == "2":
        new_lang = "en"
    else:
        input(red(t("invalid_option")))
        return
    
    # Atualizar configuração
    config = load_config()
    config["language"] = new_lang
    save_config(config)
    
    # Atualizar idioma no sistema
    set_language(new_lang)
    
    print(green("\n" + t("lang_set").format(new_lang)))
    input(yellow("\n" + t("enter_return")))

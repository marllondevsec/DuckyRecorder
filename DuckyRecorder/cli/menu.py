from DuckyRecorder.core.colors import green, red, yellow, cyan
from DuckyRecorder.utils.console import clear
from DuckyRecorder.core.recorder import Recorder
from DuckyRecorder.exporters import EXPORTERS

import time
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")


def main_menu():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    while True:
        clear()
        print(cyan("╔════════════════════════╗"))
        print(cyan("║     DuckyRecorder      ║"))
        print(cyan("╚════════════════════════╝\n"))

        print(green("1) Iniciar gravação"))
        print(green("2) Listar gravações"))
        print(green("3) Exportar gravação"))
        print(red("0) Sair\n"))

        choice = input(yellow("> ")).strip()

        if choice == "1":
            start_recording()
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            export_recording()
        elif choice == "0":
            clear()
            print(red("Saindo..."))
            break
        else:
            input(red("Opção inválida. ENTER para continuar"))


# --------------------------------------------------

def start_recording():
    clear()
    recorder = Recorder()

    print(green("🎙️  Gravação iniciada"))
    print(yellow("Pressione ENTER para parar...\n"))

    recorder.start()
    input()
    recorder.stop()

    filename = f"recording_{int(time.time())}.json"
    path = os.path.join(RECORDINGS_DIR, filename)
    recorder.save(path)

    print(green(f"\nGravação salva em: {path}"))
    input(yellow("\nENTER para voltar ao menu"))


# --------------------------------------------------

def list_recordings():
    clear()
    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".json")]

    if not files:
        print(red("Nenhuma gravação encontrada"))
    else:
        print(green("Gravações disponíveis:\n"))
        for f in files:
            print(f" - {f}")

    input(yellow("\nENTER para voltar ao menu"))


# --------------------------------------------------

def export_recording():
    clear()
    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".json")]

    if not files:
        print(red("Nenhuma gravação para exportar"))
        input(yellow("\nENTER para voltar"))
        return

    print(green("Selecione uma gravação:\n"))
    for i, f in enumerate(files):
        print(f"{i + 1}) {f}")

    try:
        choice = int(input(yellow("\nNúmero: "))) - 1
        selected = files[choice]
    except (ValueError, IndexError):
        input(red("Seleção inválida. ENTER para voltar"))
        return

    input_path = os.path.join(RECORDINGS_DIR, selected)

    # -------- escolher exporter --------
    clear()
    print(green("Selecione o formato de exportação:\n"))

    exporter_keys = list(EXPORTERS.keys())
    for i, key in enumerate(exporter_keys):
        print(f"{i + 1}) {EXPORTERS[key]['label']}")

    try:
        choice = int(input(yellow("\nNúmero: "))) - 1
        exporter = EXPORTERS[exporter_keys[choice]]
    except (ValueError, IndexError):
        input(red("Seleção inválida. ENTER para voltar"))
        return

    output_path = input_path.replace(".json", exporter["ext"])
    exporter["func"](input_path, output_path)

    print(green("\nExportado com sucesso:"))
    print(yellow(output_path))
    input(yellow("\nENTER para voltar ao menu"))

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LANG_DIR = os.path.join(BASE_DIR, "lang")

def load_language(lang: str = "pt") -> dict:
    file_path = os.path.join(LANG_DIR, f"{lang}.json")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Idioma não encontrado: {lang}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

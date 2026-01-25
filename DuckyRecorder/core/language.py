import json
import os
from pathlib import Path
from DuckyRecorder.config import get_language

BASE_DIR = Path(__file__).parent.parent
LANG_DIR = BASE_DIR / "lang"

class LanguageManager:
    def __init__(self):
        self.current_lang = get_language()
        self.strings = self.load()
    
    def load(self, lang: str = None):
        """Carrega as strings do idioma especificado ou do atual"""
        if lang:
            self.current_lang = lang
        
        file_path = LANG_DIR / f"{self.current_lang}.json"
        
        if not file_path.exists():
            # Fallback para inglês se o arquivo não existir
            file_path = LANG_DIR / "en.json"
            if not file_path.exists():
                raise FileNotFoundError(f"Arquivo de idioma não encontrado: {lang}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get(self, key: str, default: str = None):
        """Obtém uma string do idioma atual"""
        return self.strings.get(key, default or key)
    
    def set_language(self, lang: str):
        """Altera o idioma atual"""
        self.current_lang = lang
        self.strings = self.load(lang)
        return self.strings

# Instância global
_lang_manager = None

def get_lang_manager():
    """Retorna o gerenciador de idiomas singleton"""
    global _lang_manager
    if _lang_manager is None:
        _lang_manager = LanguageManager()
    return _lang_manager

# Funções de conveniência
def t(key: str, default: str = None) -> str:
    """Shortcut para obter uma string traduzida"""
    return get_lang_manager().get(key, default)

def set_language(lang: str):
    """Altera o idioma"""
    return get_lang_manager().set_language(lang)

def get_current_language() -> str:
    """Retorna o idioma atual"""
    return get_lang_manager().current_lang

# Compatibilidade com código existente
def load_language(lang: str = None) -> dict:
    """Função legada para compatibilidade"""
    if lang:
        set_language(lang)
    return get_lang_manager().strings

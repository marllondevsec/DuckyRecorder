import json
import os
from pathlib import Path
from DuckyRecorder.config import get_language
from DuckyRecorder.utils.logger import debug, info, warning, error

# CORREÇÃO: Caminho correto para o diretório lang
# __file__ = /home/ghostkernel/Documents/GitHub/DuckyRecorder/DuckyRecorder/core/language.py
# parent.parent.parent = /home/ghostkernel/Documents/GitHub/DuckyRecorder
BASE_DIR = Path(__file__).parent.parent.parent  # Vai até DuckyRecorder/
LANG_DIR = BASE_DIR / "DuckyRecorder" / "lang"

debug(f"LANG_DIR = {LANG_DIR}")
debug(f"Existe? {LANG_DIR.exists()}")

class LanguageManager:
    def __init__(self):
        # Primeiro obtém o idioma da configuração
        lang = get_language()
        debug(f"Idioma obtido da config = {lang}")
        if lang is None:
            lang = "pt"  # Fallback para português
        self.current_lang = lang
        self.strings = self.load()
    
    def load(self, lang: str = None):
        """Carrega as strings do idioma especificado ou do atual"""
        if lang:
            self.current_lang = lang
        
        # Garante que temos um idioma válido
        if self.current_lang is None:
            self.current_lang = "pt"
        
        file_path = LANG_DIR / f"{self.current_lang}.json"
        debug(f"Tentando carregar {file_path}")
        debug(f"Existe? {file_path.exists()}")
        
        if not file_path.exists():
            # Fallback para inglês se o arquivo não existir
            file_path = LANG_DIR / "en.json"
            debug(f"Fallback para {file_path}")
            debug(f"Existe? {file_path.exists()}")
            if not file_path.exists():
                # Se nem inglês existir, use um dicionário vazio
                error(f"Arquivo de idioma não encontrado: {self.current_lang}")
                return {}
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                debug(f"Carregado com sucesso, {len(data)} strings")
                return data
        except Exception as e:
            error(f"Erro ao carregar idioma {self.current_lang}: {e}")
            return {}
    
    def get(self, key: str, default: str = None):
        """Obtém uma string do idioma atual"""
        value = self.strings.get(key, default or key)
        # Se não encontrou, retorna a própria key para debugging
        if value == key:
            warning(f"String não encontrada para key: {key}")
        return value
    
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

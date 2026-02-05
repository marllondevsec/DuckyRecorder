import sys
import os
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Lock

class DebugLogger:
    """Logger centralizado para mensagens de debug"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.messages = []
        self.max_messages = 1000  # Limite de mensagens mantidas
        self.enabled = True
        self.log_file = None
        
        # Criar diretório de logs
        self.logs_dir = Path(__file__).parent.parent.parent.parent / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Criar arquivo de log com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"debug_{timestamp}.log"
    
    def log(self, message, level="DEBUG"):
        """Adiciona uma mensagem de log"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"{timestamp} [{level}] {message}"
        
        # Adiciona à lista de mensagens
        self.messages.append(log_entry)
        
        # Mantém apenas as últimas mensagens
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        # Escreve no arquivo
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except:
            pass
        
        # Imprime no console apenas se for debug (para não poluir o menu)
        if level == "DEBUG":
            print(f"\033[90m{log_entry}\033[0m", file=sys.stderr)
    
    def get_messages(self, last_n=50):
        """Retorna as últimas N mensagens"""
        return self.messages[-last_n:] if self.messages else []
    
    def clear(self):
        """Limpa as mensagens"""
        self.messages = []
    
    def set_enabled(self, enabled):
        """Ativa/desativa o logging"""
        self.enabled = enabled

# Instância global
logger = DebugLogger()

# Funções de conveniência
def debug(message):
    logger.log(message, "DEBUG")

def info(message):
    logger.log(message, "INFO")

def warning(message):
    logger.log(message, "WARNING")

def error(message):
    logger.log(message, "ERROR")

"""
DuckyRecorder - Ferramenta para gravação de eventos HID
Versão mínima para compatibilidade
"""

__version__ = "1.0.0"
__author__ = "MarllonDevSec"

# Reexportar funções do pacote interno para compatibilidade
from DuckyRecorder import (
    get_ducky_banner, get_compact_banner, 
    get_minimal_banner, get_banner, show_banner
)

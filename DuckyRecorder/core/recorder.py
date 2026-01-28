from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import time
import json
from datetime import datetime
from DuckyRecorder.core.events import Event, EventType
from DuckyRecorder.core.timeline import Timeline
from DuckyRecorder.core.hotkeys import get_key_from_string
import threading
from queue import Queue

class Recorder:
    def __init__(self, config=None):
        self.events = []
        self.start_time = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.is_recording = False
        self.is_paused = False
        self.config = config or {}
        self.event_queue = Queue()
        self.display_thread = None
        self.last_event_time = 0
        self.event_count = 0
        
        # Obtém teclas de atalho da configuração
        self.pause_key = get_key_from_string(self.config.get('pause_key', 'F9'))
        self.stop_key = get_key_from_string(self.config.get('stop_key', 'F10'))
        
        # Controllers para obter posição atual do mouse
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()

    def start(self, recording_name=None):
        """Inicia a gravação de eventos de teclado e mouse"""
        self.events = []
        self.start_time = time.time()
        self.last_event_time = self.start_time
        self.event_count = 0
        self.is_recording = True
        self.is_paused = False
        
        # Mostra informações iniciais
        name_display = f" '{recording_name}'" if recording_name else ""
        print(f"\n🎙️  Gravando{name_display}...")
        print(f"   Pausar: {self.config.get('pause_key', 'F9')}")
        print(f"   Parar: {self.config.get('stop_key', 'F10')}")
        
        # Inicia thread para exibir eventos em tempo real
        if self.config.get('show_live_preview', True):
            self.display_thread = threading.Thread(target=self._display_loop, daemon=True)
            self.display_thread.start()
        
        # Callback para teclado
        def on_press(key):
            if not self.is_recording:
                return False
            
            # Verifica teclas de atalho
            if key == self.pause_key:  # Pausar/Continuar
                self.is_paused = not self.is_paused
                status = "PAUSADO" if self.is_paused else "CONTINUANDO"
                self.event_queue.put(("status", f"Gravação {status}"))
                return
                
            if key == self.stop_key:  # Parar gravação
                self.is_recording = False
                self.event_queue.put(("status", "Gravação PARADA"))
                return False
            
            # Se estiver pausado, não grava
            if self.is_paused:
                return
            
            try:
                key_str = key.char
            except AttributeError:
                key_str = str(key).replace("Key.", "")
            
            current_time = time.time()
            event_data = {
                "type": "key_press",
                "key": key_str,
                "timestamp": current_time - self.start_time,
                "time": datetime.now().isoformat()
            }
            
            self.events.append(event_data)
            self.event_count += 1
            self.last_event_time = current_time
            
            # Adiciona à fila para exibição
            if self.config.get('show_live_preview', True):
                if key_str in ['enter', 'space', 'tab', 'backspace', 'esc']:
                    display_key = f"[{key_str.upper()}]"
                elif len(key_str) == 1:
                    display_key = key_str
                else:
                    display_key = f"<{key_str}>"
                
                self.event_queue.put(("key", display_key))

        # Callback para mouse
        def on_click(x, y, button, pressed):
            if not self.is_recording or not pressed or self.is_paused:
                return
            
            current_time = time.time()
            event_data = {
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": str(button).replace("Button.", ""),
                "timestamp": current_time - self.start_time,
                "time": datetime.now().isoformat()
            }
            
            self.events.append(event_data)
            self.event_count += 1
            self.last_event_time = current_time
            
            # Adiciona à fila para exibição
            if self.config.get('show_live_preview', True):
                self.event_queue.put(("click", f"{button} ({x}, {y})"))

        # Inicia listeners
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.mouse_listener = mouse.Listener(on_click=on_click)
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # Adiciona informações iniciais à fila
        if self.config.get('show_live_preview', True):
            self.event_queue.put(("status", f"🎙️  Gravando{name_display}..."))
            pause_key_display = self.config.get('pause_key', 'F9')
            stop_key_display = self.config.get('stop_key', 'F10')
            self.event_queue.put(("info", f"{pause_key_display}: Pausar/Continuar | {stop_key_display}: Parar"))

    def _display_loop(self):
        """Loop para exibir eventos em tempo real"""
        events_buffer = []
        
        while self.is_recording:
            try:
                # Limpa e atualiza a exibição
                self._update_display(events_buffer[-10:] if events_buffer else [])
                
                # Processa eventos da fila
                while not self.event_queue.empty():
                    event_type, data = self.event_queue.get_nowait()
                    
                    if event_type == "status":
                        events_buffer.append(f"📢 {data}")
                    elif event_type == "info":
                        events_buffer.append(f"ℹ️  {data}")
                    elif event_type == "key":
                        events_buffer.append(f"⌨️  Tecla: {data}")
                    elif event_type == "click":
                        events_buffer.append(f"🖱️  Clique: {data}")
                    
                    # Mantém apenas os últimos 20 eventos no buffer
                    if len(events_buffer) > 20:
                        events_buffer = events_buffer[-20:]
                
                time.sleep(0.1)
            except:
                pass

    def _update_display(self, events_to_show):
        """Atualiza a exibição dos eventos"""
        # Limpa a tela mantendo algumas linhas
        print("\033[2J\033[H", end="")  # Limpa tela e move cursor para o topo
        
        # Obtém posição atual do mouse
        mouse_x, mouse_y = self.mouse_controller.position
        
        # Mostra cabeçalho
        status = "⏸️ PAUSADO" if self.is_paused else "🔴 GRAVANDO"
        print(f"{status} | Eventos: {self.event_count} | Mouse: ({mouse_x}, {mouse_y})")
        print("─" * 60)
        
        # Mostra eventos recentes
        for event in events_to_show:
            print(f"  {event}")
        
        # Mostra rodapé
        print("─" * 60)
        pause_key = self.config.get('pause_key', 'F9')
        stop_key = self.config.get('stop_key', 'F10')
        print(f"{pause_key}: Pausar/Continuar | {stop_key}: Parar e Salvar")

    def stop(self):
        """Para a gravação"""
        self.is_recording = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        # Limpa a tela
        if self.config.get('show_live_preview', True):
            print("\033[2J\033[H", end="")

    def save(self, path: str):
        """Salva os eventos em um arquivo JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "duration": self.events[-1]["timestamp"] if self.events else 0,
                    "event_count": len(self.events),
                    "name": path.split('/')[-1].replace('.json', '')
                },
                "events": self.events
            }, f, indent=2, ensure_ascii=False)


# Função auxiliar para converter gravação em timeline
def recording_to_timeline(recording_json: dict) -> Timeline:
    timeline = Timeline()
    events = recording_json.get("events", [])
    
    # Adiciona evento para zerar mouse no início
    timeline.add(Event(EventType.MOUSE_ZERO, {}))
    
    last_x = 0
    last_y = 0
    
    for ev in events:
        # Preserva timestamp para uso posterior
        ev_timestamp = ev.get("timestamp", 0)
        
        if ev["type"] == "mouse_click":
            x = ev["x"]
            y = ev["y"]
            
            # Calcula movimento relativo
            rel_x = x - last_x
            rel_y = y - last_y
            
            # Só move se houver movimento significativo
            if abs(rel_x) > 1 or abs(rel_y) > 1:
                # Move mouse para posição
                timeline.add(Event(
                    EventType.MOUSE_MOVE,
                    {"x": rel_x, "y": rel_y, "mode": "FAST", "timestamp": ev_timestamp}
                ))
                last_x = x
                last_y = y
            
            # Clique
            timeline.add(Event(
                EventType.MOUSE_CLICK,
                {"button": ev.get("button", "left").upper(), "timestamp": ev_timestamp}
            ))
            
        elif ev["type"] == "key_press":
            key = ev["key"]
            
            # Tecla normal (caractere)
            if len(key) == 1 and key.isprintable() and key not in ['\n', '\r', '\t']:
                timeline.add(Event(
                    EventType.TEXT,
                    {"value": key, "timestamp": ev_timestamp}
                ))
            # Tecla especial
            else:
                timeline.add(Event(
                    EventType.KEY,
                    {"key": f"Key.{key.lower()}", "timestamp": ev_timestamp}
                ))
    
    return timeline

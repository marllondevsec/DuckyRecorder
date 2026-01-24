from pynput import keyboard, mouse
from pynput.keyboard import Key
import time
import json
from datetime import datetime
from DuckyRecorder.core.events import Event, EventType
from DuckyRecorder.core.timeline import Timeline

class Recorder:
    def __init__(self):
        self.events = []
        self.start_time = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.is_recording = False

    def start(self):
        """Inicia a gravação de eventos de teclado e mouse"""
        self.events = []
        self.start_time = time.time()
        self.is_recording = True
        
        # Callback para teclado
        def on_press(key):
            if not self.is_recording:
                return False
            
            try:
                key_str = key.char
            except AttributeError:
                key_str = str(key).replace("Key.", "")
            
            self.events.append({
                "type": "key_press",
                "key": key_str,
                "timestamp": time.time() - self.start_time,
                "time": datetime.now().isoformat()
            })

        # Callback para mouse
        def on_click(x, y, button, pressed):
            if not self.is_recording or not pressed:
                return
            
            self.events.append({
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": str(button).replace("Button.", ""),
                "timestamp": time.time() - self.start_time,
                "time": datetime.now().isoformat()
            })

        # Inicia listeners
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.mouse_listener = mouse.Listener(on_click=on_click)
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        print("🎙️  Gravando... (Pressione ENTER no terminal para parar)")

    def stop(self):
        """Para a gravação"""
        self.is_recording = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def save(self, path: str):
        """Salva os eventos em um arquivo JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "duration": self.events[-1]["timestamp"] if self.events else 0,
                    "event_count": len(self.events)
                },
                "events": self.events
            }, f, indent=2, ensure_ascii=False)

# Função auxiliar para converter gravação em timeline
def recording_to_timeline(recording_json: dict) -> Timeline:
    timeline = Timeline()
    
    # Adiciona evento para zerar mouse no início
    timeline.add(Event(EventType.MOUSE_ZERO, {}))
    
    for ev in recording_json.get("events", []):
        if ev["type"] == "mouse_click":
            # Move mouse para posição
            timeline.add(Event(
                EventType.MOUSE_MOVE,
                {"x": ev["x"], "y": ev["y"], "mode": "FAST"}
            ))
            # Clique
            timeline.add(Event(
                EventType.MOUSE_CLICK,
                {"button": ev.get("button", "left").upper()}
            ))
        elif ev["type"] == "key_press":
            key = ev["key"]
            # Tecla normal (caractere)
            if len(key) == 1:
                timeline.add(Event(
                    EventType.TEXT,
                    {"value": key}
                ))
            # Tecla especial
            else:
                timeline.add(Event(
                    EventType.KEY,
                    {"key": f"Key.{key.lower()}"}
                ))
    
    return timeline

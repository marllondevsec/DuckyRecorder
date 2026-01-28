from DuckyRecorder.core.events import EventType
import json


class ArduinoExporter:
    def export(self, timeline, fast_mode=True, zero_mouse=True):
        out = []
        
        # Header
        out += [
            "#include <Keyboard.h>",
            "#include <Mouse.h>",
            "",
            "void setup() {",
            "  Keyboard.begin();",
            "  Mouse.begin();",
            "  delay(1000);  // Aguarda inicialização",
            "",
        ]

        if zero_mouse:
            out.append("  // Zera posição do mouse")
            out.append("  for(int i=0; i<40; i++) {")
            out.append("    Mouse.move(-127, -127);")
            out.append("  }")
            out.append("  delay(100);")

        # Processa eventos com delays preservados
        last_timestamp = 0
        for ev in timeline:
            # Adiciona delay baseado no timestamp
            if hasattr(ev, 'timestamp') and ev.timestamp is not None:
                delay_ms = int((ev.timestamp - last_timestamp) * 1000)
                if delay_ms > 10:  # Só adiciona delays significativos
                    out.append(f"  delay({delay_ms});")
                last_timestamp = ev.timestamp
            
            if ev.type == EventType.MOUSE_MOVE:
                # Converte para movimento relativo (Arduino usa relativo)
                x = ev.data.get('x', 0)
                y = ev.data.get('y', 0)
                mode = ev.data.get('mode', 'FAST')
                
                if mode == 'FAST':
                    out.append(f"  // Move mouse para ({x}, {y})")
                    out.append("  while(x != 0 || y != 0) {")
                    out.append("    int dx = constrain(x, -127, 127);")
                    out.append("    int dy = constrain(y, -127, 127);")
                    out.append("    Mouse.move(dx, dy);")
                    out.append("    x -= dx;")
                    out.append("    y -= dy;")
                    out.append("  }")
                else:
                    out.append(f"  Mouse.move({x}, {y});")

            elif ev.type == EventType.MOUSE_CLICK:
                button = ev.data.get('button', 'LEFT')
                if button == 'LEFT':
                    out.append("  Mouse.click(MOUSE_LEFT);")
                elif button == 'RIGHT':
                    out.append("  Mouse.click(MOUSE_RIGHT);")
                else:
                    out.append("  Mouse.click(MOUSE_MIDDLE);")
                if not fast_mode:
                    out.append("  delay(50);")

            elif ev.type == EventType.TEXT:
                value = ev.data.get("value", "")
                if value == ' ':  # Espaço é tecla especial
                    out.append("  Keyboard.write(' ');")
                elif len(value) == 1 and value.isprintable():
                    out.append(f'  Keyboard.print("{value}");')
                if not fast_mode:
                    out.append("  delay(10);")

            elif ev.type == EventType.KEY:
                key = ev.data.get("key", "")
                arduino_key = self.map_key(key)
                out.append(f"  {arduino_key};")
                if not fast_mode:
                    out.append("  delay(10);")

        out += [
            "",
            "  Keyboard.end();",
            "  Mouse.end();",
            "}",
            "",
            "void loop() {}",
        ]

        return "\n".join(out)

    def map_key(self, key):
        """Mapeia teclas para comandos Arduino"""
        mapping = {
            "Key.enter": "Keyboard.write(KEY_RETURN)",
            "Key.backspace": "Keyboard.write(KEY_BACKSPACE)",
            "Key.tab": "Keyboard.write(KEY_TAB)",
            "Key.esc": "Keyboard.write(KEY_ESC)",
            "Key.space": "Keyboard.write(' ')",
            "Key.up": "Keyboard.write(KEY_UP_ARROW)",
            "Key.down": "Keyboard.write(KEY_DOWN_ARROW)",
            "Key.left": "Keyboard.write(KEY_LEFT_ARROW)",
            "Key.right": "Keyboard.write(KEY_RIGHT_ARROW)",
            "Key.delete": "Keyboard.write(KEY_DELETE)",
            "Key.home": "Keyboard.write(KEY_HOME)",
            "Key.end": "Keyboard.write(KEY_END)",
            "Key.page_up": "Keyboard.write(KEY_PAGE_UP)",
            "Key.page_down": "Keyboard.write(KEY_PAGE_DOWN)",
            "Key.caps_lock": "Keyboard.write(KEY_CAPS_LOCK)",
            "Key.f1": "Keyboard.write(KEY_F1)",
            "Key.f2": "Keyboard.write(KEY_F2)",
            "Key.f3": "Keyboard.write(KEY_F3)",
            "Key.f4": "Keyboard.write(KEY_F4)",
            "Key.f5": "Keyboard.write(KEY_F5)",
            "Key.f6": "Keyboard.write(KEY_F6)",
            "Key.f7": "Keyboard.write(KEY_F7)",
            "Key.f8": "Keyboard.write(KEY_F8)",
            "Key.f9": "Keyboard.write(KEY_F9)",
            "Key.f10": "Keyboard.write(KEY_F10)",
            "Key.f11": "Keyboard.write(KEY_F11)",
            "Key.f12": "Keyboard.write(KEY_F12)",
        }
        
        # Se for uma tecla de caractere simples
        if key.startswith("Key."):
            return mapping.get(key, f"Keyboard.write({key})")
        else:
            return f'Keyboard.print("{key}")'


def export_to_arduino(input_path: str, output_path: str, fast_mode=True, zero_mouse=True):
    from DuckyRecorder.core.recorder import recording_to_timeline

    try:
        with open(input_path, "r") as f:
            recording_json = json.load(f)
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo JSON: {e}")

    timeline = recording_to_timeline(recording_json)
    
    # Adiciona timestamps aos eventos
    events = recording_json.get("events", [])
    event_idx = 0
    
    for ev in timeline:
        if event_idx < len(events):
            # Usa timestamp do evento (em segundos desde o início)
            timestamp = events[event_idx].get("timestamp", 0)
            if timestamp is not None:
                ev.timestamp = timestamp
            # Avança índice para eventos que consomem múltiplos eventos do JSON
            if ev.type in [EventType.MOUSE_MOVE, EventType.MOUSE_CLICK]:
                event_idx += 1
            elif ev.type == EventType.TEXT:
                event_idx += 1
            elif ev.type == EventType.KEY:
                event_idx += 1
    
    exporter = ArduinoExporter()
    code = exporter.export(timeline, fast_mode=fast_mode, zero_mouse=zero_mouse)

    try:
        with open(output_path, "w") as f:
            f.write(code)
    except Exception as e:
        raise Exception(f"Erro ao escrever arquivo: {e}")

    return output_path

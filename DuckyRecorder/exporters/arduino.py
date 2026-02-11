from DuckyRecorder.core.events import EventType
import json


class ArduinoExporter:
    def __init__(self):
        self.mouse_vars_declared = False

    def export(self, timeline, fast_mode=True, zero_mouse=True):
        out = []
        
        # Header
        out += [
            "#include <Keyboard.h>",
            "#include <Mouse.h>",
            "",
            "void setup() {",
            "  // Delay de segurança para evitar execução acidental",
            "  delay(3000);",
            "  ",
            "  Keyboard.begin();",
            "  Mouse.begin();",
            "  delay(1000);  // Aguarda inicialização",
            "",
        ]

        if zero_mouse:
            out.append("  // Zera posição do mouse (move para canto superior esquerdo)")
            out.append("  for(int i=0; i<40; i++) {")
            out.append("    Mouse.move(-127, -127);")
            out.append("    delay(10); // Pequeno delay entre movimentos")
            out.append("  }")
            out.append("  delay(100);")

        # Processa eventos com delays preservados
        last_timestamp = 0
        for ev in timeline:
            # Adiciona delay baseado no timestamp
            if hasattr(ev, 'timestamp') and ev.timestamp is not None:
                delay_ms = int((ev.timestamp - last_timestamp) * 1000)
                if delay_ms > 10:
                    out.append(f"  delay({delay_ms});")
                last_timestamp = ev.timestamp
            
            if ev.type == EventType.MOUSE_MOVE:
                x = ev.data.get('x', 0)
                y = ev.data.get('y', 0)
                mode = ev.data.get('mode', 'FAST')
                
                if mode == 'FAST' and (abs(x) > 127 or abs(y) > 127):
                    out.append(f"  // Move mouse relativo ({x}, {y})")
                    out.append("  {")
                    out.append(f"    int targetX = {x};")
                    out.append(f"    int targetY = {y};")
                    out.append("    while(targetX != 0 || targetY != 0) {")
                    out.append("      int dx = constrain(targetX, -127, 127);")
                    out.append("      int dy = constrain(targetY, -127, 127);")
                    out.append("      Mouse.move(dx, dy);")
                    out.append("      delay(10); // Delay entre movimentos")
                    out.append("      targetX -= dx;")
                    out.append("      targetY -= dy;")
                    out.append("    }")
                    out.append("  }")
                else:
                    out.append(f"  Mouse.move({x}, {y});")
                    out.append("  delay(10);")

            elif ev.type == EventType.MOUSE_CLICK:
                button = ev.data.get('button', 'LEFT')
                if button == 'LEFT':
                    out.append("  Mouse.click(MOUSE_LEFT);")
                elif button == 'RIGHT':
                    out.append("  Mouse.click(MOUSE_RIGHT);")
                else:
                    out.append("  Mouse.click(MOUSE_MIDDLE);")
                out.append("  delay(50);")

            elif ev.type == EventType.TEXT:
                value = ev.data.get("value", "")
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                if value == ' ':
                    out.append("  Keyboard.write(' ');")
                elif len(value) == 1 and value.isprintable():
                    out.append(f'  Keyboard.print("{escaped_value}");')
                else:
                    out.append(f'  Keyboard.print("{escaped_value}");')
                out.append("  delay(10);")

            elif ev.type == EventType.KEY:
                key = ev.data.get("key", "")
                arduino_key = self.map_key(key)
                
                # 🔥 CORREÇÃO DEFINITIVA: Press + Release para TODAS as teclas especiais
                if arduino_key.startswith("KEY_"):
                    # Tecla especial que precisa de press + release
                    out.append(f"  Keyboard.press({arduino_key});")
                    # Delay apropriado baseado na tecla
                    if arduino_key in ["KEY_LEFT_GUI", "KEY_RETURN", "KEY_TAB"]:
                        out.append("  delay(100);")
                    else:
                        out.append("  delay(50);")
                    out.append(f"  Keyboard.release({arduino_key});")
                elif arduino_key == "SPACE":
                    out.append("  Keyboard.write(' ');")
                    out.append("  delay(10);")
                else:
                    # Comando já pronto (Keyboard.print)
                    out.append(f"  {arduino_key};")
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
        """Mapeia teclas para comandos Arduino - RETORNA APENAS NOMES DE CONSTANTES"""
        mapping = {
            "Key.enter": "KEY_RETURN",
            "Key.backspace": "KEY_BACKSPACE",
            "Key.tab": "KEY_TAB",
            "Key.esc": "KEY_ESC",
            "Key.space": "SPACE",
            "Key.up": "KEY_UP_ARROW",
            "Key.down": "KEY_DOWN_ARROW",
            "Key.left": "KEY_LEFT_ARROW",
            "Key.right": "KEY_RIGHT_ARROW",
            "Key.delete": "KEY_DELETE",
            "Key.home": "KEY_HOME",
            "Key.end": "KEY_END",
            "Key.page_up": "KEY_PAGE_UP",
            "Key.page_down": "KEY_PAGE_DOWN",
            "Key.caps_lock": "KEY_CAPS_LOCK",
            "Key.f1": "KEY_F1",
            "Key.f2": "KEY_F2",
            "Key.f3": "KEY_F3",
            "Key.f4": "KEY_F4",
            "Key.f5": "KEY_F5",
            "Key.f6": "KEY_F6",
            "Key.f7": "KEY_F7",
            "Key.f8": "KEY_F8",
            "Key.f9": "KEY_F9",
            "Key.f10": "KEY_F10",
            "Key.f11": "KEY_F11",
            "Key.f12": "KEY_F12",
            "Key.shift": "KEY_LEFT_SHIFT",
            "Key.ctrl": "KEY_LEFT_CTRL",
            "Key.alt": "KEY_LEFT_ALT",
            "Key.cmd": "KEY_LEFT_GUI",
        }
        
        # Se for uma tecla especial mapeada
        if key in mapping:
            return mapping[key]
        else:
            # Caracteres normais - retorna comando completo
            escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
            return f'Keyboard.print("{escaped_key}")'


def export_to_arduino(input_path: str, output_path: str, fast_mode=True, zero_mouse=True):
    from DuckyRecorder.core.recorder import recording_to_timeline

    try:
        with open(input_path, "r") as f:
            recording_json = json.load(f)
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo JSON: {e}")

    timeline = recording_to_timeline(recording_json)
    
    events = recording_json.get("events", [])
    event_idx = 0
    
    for ev in timeline:
        if event_idx < len(events):
            timestamp = events[event_idx].get("timestamp", 0)
            if timestamp is not None:
                ev.timestamp = timestamp
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

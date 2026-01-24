from DuckyRecorder.core.events import EventType
from DuckyRecorder.core.recorder import recording_to_timeline
import json


class ArduinoExporter:
    def export(self, timeline, fast_mode=True):
        """
        Exporta uma timeline para código Arduino HID.
        fast_mode: se True, remove delays para execução super-rápida
        """
        out = []

        # Header
        out += [
            "#include <Keyboard.h>",
            "#include <Mouse.h>",
            "",
            "void moveFast(int x, int y) {",
            "  while (x != 0 || y != 0) {",
            "    int mx = constrain(x, -127, 127);",
            "    int my = constrain(y, -127, 127);",
            "    Mouse.move(mx, my);",
            "    x -= mx;",
            "    y -= my;",
            "  }",
            "}",
            "",
            "void mouseZero() {",
            "  for (int i = 0; i < 40; i++) {",
            "    Mouse.move(-127, -127);",
            "  }",
            "}",
            "",
            "void setup() {",
            "  Keyboard.begin();",
            "  Mouse.begin();",
            f"  delay({'10' if fast_mode else '500'});",
            "",
        ]

        for ev in timeline:
            if ev.type == EventType.MOUSE_ZERO:
                out.append("  mouseZero();")

            elif ev.type == EventType.MOUSE_MOVE:
                x = ev.data['x']
                y = ev.data['y']
                out.append(f"  moveFast({x}, {y});")
                if not fast_mode:
                    out.append(f"  delay({ev.data.get('delay', 50)});")

            elif ev.type == EventType.MOUSE_CLICK:
                out.append("  Mouse.click(MOUSE_LEFT);")
                if not fast_mode:
                    out.append(f"  delay(50);")

            elif ev.type == EventType.TEXT:
                value = ev.data["value"].replace('"', '\\"')
                out.append(f'  Keyboard.print("{value}");')
                if not fast_mode:
                    out.append(f"  delay(10);")

            elif ev.type == EventType.KEY:
                out.append(f"  Keyboard.write({self.map_key(ev.data['key'])});")
                if not fast_mode:
                    out.append(f"  delay(10);")

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
        """Mapeia teclas especiais para constantes Arduino"""
        mapping = {
            "Key.enter": "KEY_RETURN",
            "Key.backspace": "KEY_BACKSPACE",
            "Key.tab": "KEY_TAB",
            "Key.esc": "KEY_ESC",
            "Key.space": "' '",
            "Key.up": "KEY_UP_ARROW",
            "Key.down": "KEY_DOWN_ARROW",
            "Key.left": "KEY_LEFT_ARROW",
            "Key.right": "KEY_RIGHT_ARROW",
        }
        return mapping.get(key, f"'{key}'" if len(key) == 1 else "0")


# Função que o CLI usa
def export_to_arduino(json_path: str, output_path: str, fast_mode: bool = True):
    """
    Lê um arquivo JSON de gravação e gera um .ino compatível com Arduino HID.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    timeline = recording_to_timeline(data)
    arduino = ArduinoExporter()
    code = arduino.export(timeline, fast_mode=fast_mode)

    with open(output_path, "w") as f:
        f.write(code)

    return output_path

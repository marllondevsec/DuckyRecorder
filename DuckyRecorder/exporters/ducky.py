import json
from pathlib import Path

KEY_MAP = {
    "Key.enter": "ENTER",
    "Key.backspace": "BACKSPACE",
    "Key.tab": "TAB",
    "Key.space": "SPACE",
    "Key.esc": "ESCAPE"
}

STRING_JOIN_THRESHOLD_MS = 300  # até aqui ainda junta string


def export_to_ducky(json_path: str, output_path: str):
    json_path = Path(json_path)
    output_path = Path(output_path)

    with open(json_path, "r") as f:
        events = json.load(f)

    lines = []
    last_time = events[0]["time"] if events else 0
    string_buffer = ""

    def flush_string():
        nonlocal string_buffer
        if string_buffer:
            lines.append(f"STRING {string_buffer}")
            string_buffer = ""

    for event in events:
        current_time = event["time"]
        delay_ms = int((current_time - last_time) * 1000)
        last_time = current_time

        # ⏱️ delay grande = pausa real → quebra string
        if delay_ms > STRING_JOIN_THRESHOLD_MS:
            flush_string()
            lines.append(f"DELAY {delay_ms}")

        if event["type"] == "mouse_click":
            flush_string()
            lines.append(f"REM MOUSE CLICK {event['x']} {event['y']}")

        elif event["type"] == "key_press":
            key = event["key"]

            # 🔑 tecla especial
            if key in KEY_MAP:
                flush_string()
                lines.append(KEY_MAP[key])

            # 🔕 outras Key.*
            elif key.startswith("Key."):
                flush_string()
                lines.append(f"REM UNSUPPORTED {key}")

            # 🔤 caractere normal → junta
            else:
                string_buffer += key

    flush_string()
    output_path.write_text("\n".join(lines))
    return output_path

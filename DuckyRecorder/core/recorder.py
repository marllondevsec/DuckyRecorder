from DuckyRecorder.core.events import Event, EventType
from DuckyRecorder.core.timeline import Timeline

class Recorder:
    def __init__(self):
        self.recording = []

    def start(self):
        # Aqui a lógica para iniciar gravação real
        pass

    def stop(self):
        # Aqui a lógica para parar gravação real
        pass

    def save(self, path: str):
        import json
        with open(path, "w") as f:
            json.dump(self.recording, f, indent=2)

# Função auxiliar para converter gravação em timeline
def recording_to_timeline(recording_json: list) -> Timeline:
    timeline = Timeline()
    timeline.add(Event(EventType.MOUSE_ZERO, {}))

    for ev in recording_json:
        if ev["type"] == "mouse_click":
            timeline.add(Event(
                EventType.MOUSE_MOVE,
                {"x": ev["x"], "y": ev["y"], "mode": "FAST"}
            ))
            timeline.add(Event(
                EventType.MOUSE_CLICK,
                {"button": "LEFT"}
            ))
        elif ev["type"] == "key_press":
            key = ev["key"]
            if len(key) == 1:
                timeline.add(Event(
                    EventType.TEXT,
                    {"value": key}
                ))
            else:
                timeline.add(Event(
                    EventType.KEY,
                    {"key": key}
                ))

    return timeline

class Timeline:
    def __init__(self):
        self.events = []

    def add(self, event):
        self.events.append(event)

    def __iter__(self):
        return iter(self.events)

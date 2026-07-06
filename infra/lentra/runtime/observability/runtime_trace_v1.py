class RuntimeTraceV1:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)

    def get(self):
        return self.events

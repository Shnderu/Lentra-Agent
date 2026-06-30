class TraceStore:

    def __init__(self):
        self.events = []

    def push(self, event):
        self.events.append(event)

    def get_all(self):
        return self.events

    def clear(self):
        self.events = []

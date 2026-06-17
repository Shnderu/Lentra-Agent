class ReplayStore:

    def __init__(self):
        self.events = []

    def save(self, event):
        self.events.append(event)

    def get(self, idx):
        return self.events[idx]

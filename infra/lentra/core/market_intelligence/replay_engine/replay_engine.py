class ReplayEngine:
    """
    STEP 9: rebuild state from events (future foundation for analytics)
    """

    def __init__(self):
        self.events = []

    def append(self, event: dict):
        self.events.append(event)

    def replay(self):
        state = {}

        for event in self.events:
            payload = event["payload"]
            key = payload.get("location", "unknown")

            state[key] = payload

        return state

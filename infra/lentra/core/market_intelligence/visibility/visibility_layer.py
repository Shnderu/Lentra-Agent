from lentra.core.market_intelligence.visibility.visibility_stream import VisibilityStream


class VisibilityLayer:

    def __init__(self):
        self.stream = VisibilityStream()

    def event(self, event_type: str, payload: dict):
        self.stream.emit(event_type, payload)

    def snapshot(self):
        return self.stream.dump()

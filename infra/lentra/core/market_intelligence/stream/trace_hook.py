from lentra.core.market_intelligence.stream.global_stream import get_stream


class TraceHook:

    def __init__(self):
        self.stream = get_stream()

    def emit(self, event_type: str, payload: dict):
        self.stream.publish({
            "type": event_type,
            "payload": payload
        })

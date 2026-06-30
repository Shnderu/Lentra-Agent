import json
from typing import Callable, List


class StreamBus:
    """
    UI streaming layer (in-memory MVP)
    """

    def __init__(self):
        self.subscribers: List[Callable] = []

    def subscribe(self, fn: Callable):
        self.subscribers.append(fn)

    def publish(self, event_type: str, payload):
        event = {
            "type": event_type,
            "payload": payload
        }

        for sub in self.subscribers:
            try:
                sub(json.dumps(event))
            except Exception:
                pass

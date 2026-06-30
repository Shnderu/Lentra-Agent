from typing import List, Dict, Any
import time


class EventLog:
    """
    VISIBILITY LAYER: in-memory event store
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def append(self, event: dict):
        event = dict(event)
        event["ts"] = time.time()
        self.events.append(event)

    def all(self):
        return self.events

    def clear(self):
        self.events = []

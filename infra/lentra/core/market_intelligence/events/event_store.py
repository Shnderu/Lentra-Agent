from typing import List, Dict, Any
import time


class EventStore:
    """
    SIMPLE IN-MEMORY EVENT GRAPH STORAGE
    (archaeology v2 layer)
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def emit(self, event_type: str, payload: dict):
        self.events.append({
            "type": event_type,
            "payload": payload,
            "ts": time.time()
        })

    def all(self):
        return self.events

    def clear(self):
        self.events = []

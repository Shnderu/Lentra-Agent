from typing import List, Dict, Any
from lentra.core.market_intelligence.visibility.event import VisibilityEvent


class VisibilityBus:
    """
    In-memory real-time event stream for AI OS observability
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def emit(self, event: VisibilityEvent):
        self.events.append({
            "type": event.type.value,
            "payload": event.payload,
            "ts": event.ts
        })

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []

# ============================================================
# EVENT STORAGE V16.6
# ============================================================

from typing import List
from lentra.events.models import Event


class EventStore:
    def __init__(self):
        self.events: List[Event] = []

    def add(self, event: Event):
        self.events.append(event)

    def get_user_events(self, user_id: str):
        return [e for e in self.events if e.user_id == user_id]

# ============================================================
# EVENT COLLECTOR V16.6
# ============================================================

from lentra.events.models import Event


class EventCollector:
    def __init__(self, store):
        self.store = store

    def track(self, user_id: str, event_type: str, listing_id: str, meta=None):
        event = Event(
            user_id=user_id,
            event_type=event_type,
            listing_id=listing_id,
            meta=meta or {}
        )

        self.store.add(event)
        return event

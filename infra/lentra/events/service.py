# ============================================================
# EVENT SERVICE V16.6
# ============================================================

from lentra.events.storage.memory import EventStore
from lentra.events.collectors.collector import EventCollector
from lentra.events.processor.feedback import FeedbackProcessor


class EventService:
    def __init__(self):
        self.store = EventStore()
        self.collector = EventCollector(self.store)
        self.processor = FeedbackProcessor()

    def track_event(self, user_id, event_type, listing_id):
        return self.collector.track(user_id, event_type, listing_id)

    def get_signals(self, user_id):
        events = self.store.get_user_events(user_id)
        return self.processor.build_signals(events)

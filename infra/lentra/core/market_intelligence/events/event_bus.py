from lentra.core.market_intelligence.visibility.visibility_bus import VisibilityBus

class EventBus:
    """
    Backward-compatible event bus
    """

    def __init__(self):
        self.bus = VisibilityBus()

    def publish(self, event_type: str, payload: dict):
        # safe fallback - no breaking
        self.bus.events.append({
            "type": event_type,
            "payload": payload
        })

    def dump(self):
        return self.bus.get_events()

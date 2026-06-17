from collections import defaultdict
from typing import Callable, Dict, List
from app.core.events import Event


class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Event], None]):
        self.handlers[event_type].append(handler)

    def publish(self, event: Event):
        print(f"[BUS] event={event.type} trace={event.trace_id} payload={event.payload}")

        if event.type not in self.handlers:
            print(f"[LEAK] no handlers for event={event.type}")
            return

        for h in self.handlers[event.type]:
            try:
                h(event)
            except Exception as e:
                print(f"[ERROR] handler_failed event={event.type} err={e}")

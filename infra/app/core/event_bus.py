from collections import defaultdict
from typing import Callable, Dict, List
from app.core.events import Event
from app.core.trace import Span
import time


class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Event], None]):
        self.handlers[event_type].append(handler)

    def publish(self, event: Event, span: Span = None):
        if span:
            span.start(f"bus_publish_{event.type}")

        print(f"[BUS] event={event.type} trace={event.trace_id}")

        if event.type not in self.handlers:
            print(f"[LEAK] no handlers for event={event.type}")
            if span:
                span.end(f"bus_publish_{event.type}")
            return

        for h in self.handlers[event.type]:
            try:
                h(event, span)
            except Exception as e:
                print(f"[ERROR] handler_failed event={event.type} err={e}")

        if span:
            span.end(f"bus_publish_{event.type}")

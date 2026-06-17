from collections import defaultdict
from typing import Callable, Dict, List
from app.core.events import Event


class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler):
        self.handlers[event_type].append(handler)

    def publish(self, event: Event, span=None, graph=None, parent=None):
        print(f"[BUS] {event.type} trace={event.trace_id}")

        if parent and graph:
            graph.link(parent.type, event.type)

        if event.type not in self.handlers:
            print(f"[LEAK] no handler for {event.type}")
            return

        for h in self.handlers[event.type]:
            try:
                return h(event, span, graph)
            except Exception as e:
                print(f"[ERROR] {e}")

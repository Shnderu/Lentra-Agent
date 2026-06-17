from collections import defaultdict
from typing import Callable, Dict, List
import time


class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler):
        self.handlers[event_type].append(handler)

    def publish(self, event, span=None, graph=None, parent=None):
        print(f"[BUS] {event.type} trace={event.trace_id}")

        if parent and graph:
            graph.link(parent.type, event.type)

        if event.type not in self.handlers:
            print("[LEAK] no handler")
            return

        for h in self.handlers[event.type]:
            retries = 1

            for attempt in range(retries + 1):
                try:
                    start = time.time()

                    result = h(event, span, graph)

                    dt = time.time() - start
                    print(f"[BUS] handler_latency={dt:.3f}s")

                    return result

                except Exception as e:
                    print(f"[BUS ERROR] attempt={attempt} err={e}")

                    time.sleep(0.05)

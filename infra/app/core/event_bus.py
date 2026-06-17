from collections import defaultdict
from typing import Callable, Dict, List


class EventBus:
    def __init__(self, executor, dlq):
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.executor = executor
        self.dlq = dlq

    def subscribe(self, event_type: str, handler):
        self.handlers[event_type].append(handler)

    def publish(self, event, span=None, graph=None, parent=None):
        print(f"[BUS] {event.type} trace={event.trace_id}")

        if parent and graph:
            graph.link(parent.type, event.type)

        if event.type not in self.handlers:
            print("[LEAK] no handler")
            self.dlq.push(event, "no_handler")
            return

        for h in self.handlers[event.type]:
            future = self.executor.submit(h, event, span, graph)

            if future is None:
                self.dlq.push(event, "backpressure_drop")
                return

            try:
                return future.result(timeout=2)
            except Exception as e:
                print(f"[EXEC ERROR] {e}")
                self.dlq.push(event, str(e))

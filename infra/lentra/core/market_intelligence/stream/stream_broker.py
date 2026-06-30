from typing import List, Callable, Any


class StreamBroker:
    """
    SIMPLE PUB/SUB STREAM LAYER FOR AI OS EVENTS
    """

    def __init__(self):
        self.subscribers: List[Callable[[dict], Any]] = []

    def subscribe(self, fn: Callable[[dict], Any]):
        self.subscribers.append(fn)

    def publish(self, event: dict):
        for sub in self.subscribers:
            try:
                sub(event)
            except Exception:
                # NEVER BREAK PIPELINE
                pass

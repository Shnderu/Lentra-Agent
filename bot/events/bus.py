from collections import defaultdict
from typing import Callable, Dict, List, Any

EVENTS: Dict[str, List[Callable]] = defaultdict(list)


def subscribe(event: str, handler: Callable):
    EVENTS[event].append(handler)


def publish(event: str, payload: Any = None):
    for handler in EVENTS.get(event, []):
        try:
            handler(payload)
        except Exception as e:
            print(f"[EVENT ERROR] {e}")

from collections import deque
from typing import List, Dict, Any


class VisibilityStream:
    """
    In-memory realtime debug stream
    """

    def __init__(self, max_size: int = 1000):
        self.buffer = deque(maxlen=max_size)

    def emit(self, event_type: str, payload: Dict[str, Any]):
        self.buffer.append({
            "type": event_type,
            "payload": payload
        })

    def dump(self) -> List[Dict[str, Any]]:
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()

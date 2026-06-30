import time
import uuid
from typing import Dict, Any


class TraceContext:
    """
    End-to-end execution trace container
    """

    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.events = []

    def log(self, stage: str, data: Dict[str, Any]):
        self.events.append({
            "stage": stage,
            "ts": time.time(),
            "data": data
        })

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "events": self.events
        }

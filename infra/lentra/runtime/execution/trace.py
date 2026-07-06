import time
import uuid
from typing import Dict, Any, List


class ExecutionTrace:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.events: List[Dict[str, Any]] = []

    def emit(self, event_type: str, payload: dict):
        self.events.append({
            "ts": time.time(),
            "trace_id": self.trace_id,
            "event": event_type,
            "payload": payload
        })

    def get(self):
        return {
            "trace_id": self.trace_id,
            "events": self.events
        }

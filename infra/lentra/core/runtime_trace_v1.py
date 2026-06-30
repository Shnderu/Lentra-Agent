import time
import uuid
import threading
from typing import Dict, Any, Optional, List


class RuntimeTraceV1:
    """
    TRACE GRAPH v1 (read-only instrumentation layer)
    """

    def __init__(self, registry=None):
        self.trace_id = str(uuid.uuid4())
        self.events: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

        self.registry = registry
        if self.registry:
            self.registry.register(self)

    def emit(self, node: str, event: str, payload: Optional[Dict[str, Any]] = None):
        record = {
            "ts": time.time(),
            "trace_id": self.trace_id,
            "node": node,
            "event": event,
            "payload": payload or {}
        }

        with self._lock:
            self.events.append(record)

        return record

    def enter(self, node: str, payload=None):
        return self.emit(node, "enter", payload)

    def exit(self, node: str, payload=None):
        return self.emit(node, "exit", payload)

    def error(self, node: str, error: str):
        return self.emit(node, "error", {"error": error})

    def route(self, node: str, payload=None):
        return self.emit(node, "route", payload)

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "events": self.events
        }

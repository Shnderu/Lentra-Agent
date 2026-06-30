"""
TRACE LAYER v1 (non-invasive)

PURPOSE:
- capture execution flow
- validate canonical execution graph
- detect hidden cycles

NO BUSINESS LOGIC HERE
"""

from typing import Dict, Any
import time


class TraceLayer:

    def __init__(self):
        self.events = []

    def emit(self, node: str, payload: Dict[str, Any] = None):
        event = {
            "ts": time.time(),
            "node": node,
            "payload": payload or {}
        }

        self.events.append(event)

        # lightweight stdout trace (safe)
        print(f"[TRACE] {node}")

    def get_trace(self):
        return self.events

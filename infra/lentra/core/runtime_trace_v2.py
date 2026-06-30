import time
import uuid
from typing import Dict, Any, Optional, List


class RuntimeTraceV2:
    """
    TRACE GRAPH v2 (correlated execution tracing)
    """

    def __init__(self, graph=None):
        self.trace_id = str(uuid.uuid4())
        self.events: List[Dict[str, Any]] = []
        self.graph = graph

    def emit(self, node: str, event: str, payload=None):
        record = {
            "ts": time.time(),
            "trace_id": self.trace_id,
            "node": node,
            "event": event,
            "payload": payload or {}
        }

        self.events.append(record)

        if self.graph:
            self.graph.add_node(node, event, self.trace_id, payload)

        return record

    def link(self, source: str, target: str, relation: str):
        if self.graph:
            self.graph.add_edge(source, target, relation)

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "events": self.events
        }

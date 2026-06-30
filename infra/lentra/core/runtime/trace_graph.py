"""
TRACE GRAPH BUILDER v1 (instrumentation layer)

Purpose:
- runtime execution graph tracing
- lightweight event + edge tracking
- NO business logic, only observability
"""

from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import json


class TraceGraph:
    """
    Minimal runtime execution graph collector
    """

    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.meta: Dict[str, Any] = {
            "started_at": datetime.utcnow().isoformat()
        }

    # -------------------------
    # CORE TRACE EVENTS
    # -------------------------

    def emit(self, layer: str, event: str, payload: Optional[Dict[str, Any]] = None):
        """
        Record a node execution event
        """
        node = {
            "ts": datetime.utcnow().isoformat(),
            "layer": layer,
            "event": event,
            "payload": payload or {}
        }
        self.nodes.append(node)

        print(f"[TRACE] {layer}.{event}")

    def link(self, src: str, dst: str, relation: str = "calls"):
        """
        Record execution edge between components
        """
        edge = {
            "ts": datetime.utcnow().isoformat(),
            "from": src,
            "to": dst,
            "relation": relation
        }
        self.edges.append(edge)

        print(f"[TRACE-LINK] {src} -> {dst} ({relation})")

    # -------------------------
    # INTROSPECTION
    # -------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "meta": self.meta,
            "nodes": self.nodes,
            "edges": self.edges
        }

    def dump(self, pretty: bool = True):
        data = self.snapshot()

        if pretty:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(data, ensure_ascii=False))

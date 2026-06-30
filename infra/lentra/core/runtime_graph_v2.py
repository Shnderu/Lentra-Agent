from typing import Dict, List, Any


class RuntimeGraphV2:
    """
    TRACE GRAPH v2 (execution graph builder)

    PURPOSE:
    - build causal execution graph from trace events
    """

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node: str, event: str, trace_id: str, payload=None):
        self.nodes.append({
            "node": node,
            "event": event,
            "trace_id": trace_id,
            "payload": payload or {}
        })

    def add_edge(self, source: str, target: str, relation: str):
        self.edges.append({
            "from": source,
            "to": target,
            "relation": relation
        })

    def build(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

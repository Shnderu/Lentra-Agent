import time
import uuid


class Trace:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.nodes = []
        self.edges = []
        self._last_node = None

    def node(self, name: str, meta=None):
        node_id = f"{name}:{len(self.nodes)}"

        self.nodes.append({
            "id": node_id,
            "name": name,
            "meta": meta or {},
            "ts": time.time()
        })

        if self._last_node:
            self.edges.append({
                "from": self._last_node,
                "to": node_id
            })

        self._last_node = node_id

        return node_id

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "nodes": self.nodes,
            "edges": self.edges
        }

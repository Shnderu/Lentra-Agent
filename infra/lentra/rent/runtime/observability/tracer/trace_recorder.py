import time
import uuid


class TraceRecorder:

    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.nodes = []
        self.edges = []

    def node(self, name: str, meta: dict = None):
        self.nodes.append({
            "id": name,
            "meta": meta or {},
            "ts": time.time()
        })

    def edge(self, a: str, b: str):
        self.edges.append({
            "from": a,
            "to": b
        })

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "nodes": self.nodes,
            "edges": self.edges
        }

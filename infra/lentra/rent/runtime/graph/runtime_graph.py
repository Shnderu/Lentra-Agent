import time
import uuid


class RuntimeGraph:
    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.nodes = []
        self.edges = []

        self._start_times = {}

    def add_node(self, name: str, meta: dict = None):
        now = time.time()

        node_id = f"{name}:{len(self.nodes)}"

        self._start_times[node_id] = now

        node = {
            "id": node_id,
            "name": name,
            "meta": meta or {},
            "ts": now,
            "trace_id": self.trace_id
        }

        self.nodes.append(node)
        return node_id

    def finish_node(self, node_id: str):
        now = time.time()
        start = self._start_times.get(node_id, now)

        latency = round((now - start) * 1000, 3)

        for n in self.nodes:
            if n["id"] == node_id:
                n["latency_ms"] = latency

    def add_edge(self, frm: str, to: str):
        self.edges.append({
            "from": frm,
            "to": to
        })

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "nodes": self.nodes,
            "edges": self.edges
        }

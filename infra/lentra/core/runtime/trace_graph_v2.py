import uuid


class RuntimeTraceV2:

    def __init__(self, trace_id=None):

        # FIX: auto-generate if missing
        self.trace_id = trace_id or str(uuid.uuid4())

        self.nodes = []
        self.edges = []

    def emit(self, layer: str, event: str, payload: dict = None):

        node_id = f"{self.trace_id}:{layer}.{event}"

        self.nodes.append({
            "id": node_id,
            "layer": layer,
            "event": event,
            "payload": payload or {}
        })

        return node_id

    def link(self, a: str, b: str, relation: str):

        self.edges.append({
            "from": a,
            "to": b,
            "type": relation
        })

    def dump(self):
        return {
            "trace_id": self.trace_id,
            "nodes": self.nodes,
            "edges": self.edges
        }

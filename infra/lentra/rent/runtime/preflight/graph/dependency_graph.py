class DependencyGraph:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name: str, obj):
        self.nodes[name] = obj

    def add_edge(self, a: str, b: str):
        self.edges.append((a, b))

    def validate(self):
        missing = []

        for name, obj in self.nodes.items():
            if obj is None:
                missing.append(name)

        if missing:
            raise RuntimeError(f"[BOOT GRAPH INVALID] missing: {missing}")

        return True

    def dump(self):
        return {
            "nodes": list(self.nodes.keys()),
            "edges": self.edges
        }

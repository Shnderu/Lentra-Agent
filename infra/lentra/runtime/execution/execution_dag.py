from collections import defaultdict


class ExecutionDAG:
    def __init__(self):
        self.graph = defaultdict(list)

    def link(self, from_node: str, to_node: str):
        self.graph[from_node].append(to_node)

    def get(self):
        return dict(self.graph)

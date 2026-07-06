from collections import defaultdict


class CycleError(Exception):
    pass


class DAGValidator:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.stack = set()

    def validate(self):
        for node in self.graph:
            if node not in self.visited:
                self._dfs(node)

    def _dfs(self, node):
        self.visited.add(node)
        self.stack.add(node)

        for neigh in self.graph.get(node, []):
            if neigh in self.stack:
                raise CycleError(f"[ARCH DAG] cycle detected: {node} -> {neigh}")

            if neigh not in self.visited:
                self._dfs(neigh)

        self.stack.remove(node)

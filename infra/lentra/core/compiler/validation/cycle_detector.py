from collections import defaultdict


class CycleError(Exception):
    pass


class CycleDetector:

    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.stack = set()

    def dfs(self, node):

        if node in self.stack:
            raise CycleError(f"[CYCLE DETECTED] {node}")

        if node in self.visited:
            return

        self.visited.add(node)
        self.stack.add(node)

        for dep in self.graph.get(node, []):
            self.dfs(dep)

        self.stack.remove(node)

    def validate(self):
        for node in self.graph:
            self.dfs(node)

        return True

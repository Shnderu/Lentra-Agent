from app.core.graph.node import GraphNode


class ExecutionGraph:

    def __init__(self):
        self.nodes = {}

    def add_node(self, node: GraphNode):
        self.nodes[node.name] = node

    def get(self, name: str):
        return self.nodes.get(name)

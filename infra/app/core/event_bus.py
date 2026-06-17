from app.core.graph.execution_graph import ExecutionGraph
from app.core.graph.engine import GraphEngine
from app.core.graph.build_graph import build_graph


class EventBus:

    def __init__(self):
        self.graph = ExecutionGraph()

        nodes = build_graph()

        for n in nodes.values():
            self.graph.add_node(n)

        self.engine = GraphEngine(self.graph)

    def publish(self, event, span, graph=None):

        result = self.engine.run("INTENT", event, span)

        return result

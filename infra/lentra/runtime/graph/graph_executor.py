from lentra.core.market_intelligence.graph.integration import GraphIntegration

class GraphExecutor:

    def __init__(self):
        self.graph = GraphIntegration()

    def execute(self, data):
        model = self.graph.build(data)

        return {
            "status": "executed",
            "graph": model
        }

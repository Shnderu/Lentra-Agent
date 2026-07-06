class GraphPluginRuntime:

    def execute(self, graph):
        return {
            "status": "executed",
            "graph": graph
        }

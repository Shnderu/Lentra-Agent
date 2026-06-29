from lentra.core.graph.state_runtime_v1 import state_graph_runtime


class PipelineDefinitionV1:

    def execute(self, intent: dict):
        """
        intent: нормализованный dict вида:
        {
            "name": "...",
            "confidence": ...,
            "payload": {...},
            "scenarios": [...]
        }
        """

        return state_graph_runtime.execute(intent)


pipeline = PipelineDefinitionV1()

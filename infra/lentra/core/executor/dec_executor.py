from lentra.core.graph.engine import ExecutionEngine as GraphExecutionEngine


class ExecutionEngine:
    """
    Adapter layer between FlowGlue and Graph ExecutionEngine
    """

    def __init__(self, registry):
        self.registry = registry
        self._engine = GraphExecutionEngine()

    def run(self, flow):
        """
        Executes flow via graph engine.
        Must remain SYNC (no await in worker layer)
        """

        if flow is None:
            raise ValueError("Flow is None")

        # normalize flow to dict if needed
        if hasattr(flow, "to_dict"):
            payload = flow.to_dict()
        elif isinstance(flow, dict):
            payload = flow
        else:
            payload = {"flow": str(flow)}

        return self._engine.run(payload)

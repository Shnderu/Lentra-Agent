class GraphRuntimeV1:
    """
    DISABLED GRAPH RUNTIME
    """

    def run(self, *args, **kwargs):
        raise RuntimeError(
            "Graph runtime is disabled. Execution is handled by pipeline only."
        )

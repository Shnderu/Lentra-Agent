class GraphCompiler:
    """
    OFFLINE ONLY COMPILER
    """

    def compile(self, graph):
        return {
            "compiled": True,
            "execution_mode": "offline_only",
            "graph": graph
        }

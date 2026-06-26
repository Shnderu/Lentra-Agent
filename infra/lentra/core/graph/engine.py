"""
GRAPH ENGINE ISOLATED MODE

АРХИТЕКТУРНОЕ ПРАВИЛО:
- Graph НЕ участвует в runtime execution
- Graph НЕ вызывается pipeline/executor
- Graph используется только оффлайн (analysis / compile)
"""

class GraphEngine:
    """
    DISABLED RUNTIME EXECUTION ENGINE
    """

    def __init__(self):
        self.enabled = False

    def execute(self, *args, **kwargs):
        raise RuntimeError(
            "Graph execution is disabled. "
            "Use pipeline as single execution authority."
        )

    def compile(self, graph_definition):
        """
        Allowed: static compilation only
        """
        return {
            "status": "compiled",
            "mode": "offline",
            "graph": graph_definition
        }

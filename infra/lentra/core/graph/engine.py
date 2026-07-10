"""
OFFLINE GRAPH COMPILER

ARCHITECTURE RULES:

- Graph is not runtime execution
- Graph is not pipeline authority
- Graph is offline analysis/compiler layer only
"""


class OfflineGraphCompiler:
    """
    Static graph compiler.

    Allowed:
    - graph validation
    - graph compilation
    - offline analysis

    Forbidden:
    - runtime execution
    - task orchestration
    """

    def __init__(self):
        self.enabled = False

    def compile(self, graph_definition):

        return {
            "status": "compiled",
            "mode": "offline",
            "graph": graph_definition,
        }

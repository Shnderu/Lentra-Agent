from typing import Dict, Any


class GraphAdapter:
    """
    Graph layer adapter.

    Responsibility:
    - graph representation only
    - no intelligence execution
    - no gateway dependency

    Graph is a feature/context layer between
    Market Intelligence and Decision Layer.
    """

    def __init__(self, builder):
        self.builder = builder

    def build_graph(
        self,
        pricing: Dict[str, Any],
        risk: Dict[str, Any],
        signal: Dict[str, Any]
    ):
        return self.builder.build(
            pricing,
            risk,
            signal
        )

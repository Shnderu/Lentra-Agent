from typing import Dict, Any


class GraphAdapter:
    """
    Minimal stable adapter for graph execution layer.
    """

    def __init__(self, builder):
        self.builder = builder

    def build_graph(self, pricing: Dict[str, Any], risk: Dict[str, Any], signal: Dict[str, Any]):
        return self.builder.build(pricing, risk, signal)

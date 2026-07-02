from typing import Dict, Any
from .intelligence_graph_runtime import IntelligenceGraphRuntime


class GraphPlugin:
    """
    SAFE OS INTELLIGENCE GRAPH LAYER v1

    - non-breaking
    - plugin wrapper over engines
    - does NOT replace gateway
    """

    def __init__(self):
        self.runtime = IntelligenceGraphRuntime()

    def evaluate(self, engines: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.runtime.execute(engines, payload)

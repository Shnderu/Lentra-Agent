from typing import Dict, List

from lentra.core.market_intelligence.graph_v2.router import GraphRouter
from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutorV1


class BridgeV4Pipeline:
    """
    Full deterministic pipeline:
    GraphV2 → Bridge planning → Aider execution
    """

    def __init__(self):
        self.router = GraphRouter()
        self.executor = AiderDeterministicExecutorV1()

    # -------------------------
    # PLAN STAGE
    # -------------------------

    def build_plan(self, query: str) -> Dict:
        routing = self.router.route(query)

        return {
            "query": query,
            "intent": routing["intent"],
            "nodes": routing["selected_node"],
            "symbols": routing["selected_symbols"],
            "files": routing["selected_files"],
        }

    # -------------------------
    # EXECUTION STAGE
    # -------------------------

    def run(self, query: str) -> Dict:
        plan = self.build_plan(query)

        files = plan["files"]

        result = self.executor.run(
            instruction=query,
            files=files
        )

        return {
            "plan": plan,
            "execution": result
        }

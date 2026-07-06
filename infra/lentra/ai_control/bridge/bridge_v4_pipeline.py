from typing import Dict

from lentra.core.market_intelligence.graph_v2.router import GraphRouter
from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutorV1
from lentra.ai_control.bridge.auto_checkpoint import AutoCheckpoint


class BridgeV4Pipeline:
    """
    Full deterministic pipeline with auto git checkpointing.
    """

    def __init__(self):
        self.router = GraphRouter()
        self.executor = AiderDeterministicExecutorV1()
        self.checkpoint = AutoCheckpoint()

    def build_plan(self, query: str) -> Dict:
        routing = self.router.route(query)

        return {
            "query": query,
            "intent": routing["intent"],
            "nodes": routing["selected_node"],
            "symbols": routing["selected_symbols"],
            "files": routing["selected_files"],
        }

    def run(self, query: str) -> Dict:
        # 🔒 NEW: auto checkpoint BEFORE execution
        self.checkpoint.ensure_clean()

        plan = self.build_plan(query)

        result = self.executor.run(
            instruction=query,
            files=plan["files"],
        )

        return {
            "plan": plan,
            "execution": result,
        }

from lentra.ai_control.bridge.bridge_v4 import BridgeV4
from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutor


class BridgeV4Pipeline:

    def __init__(self, graph_router=None):
        self.bridge = BridgeV4(graph_router)
        self.executor = AiderDeterministicExecutor()

    def run(self, query: str):

        plan = self.bridge.run(query)

        files = plan["plan"]["expanded_files"]

        return self.executor.run(
            prompt=query,
            files=files
        )

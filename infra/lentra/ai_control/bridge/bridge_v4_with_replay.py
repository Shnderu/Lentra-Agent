from lentra.ai_control.bridge.bridge_v4 import BridgeV4
from lentra.ai_control.execution.replay.replay_engine_v1 import ReplayEngineV1
from lentra.ai_control.execution.ledger.execution_ledger_v1 import ExecutionLedgerV1


class BridgeV4WithReplay:
    """
    BridgeV4 + Replay capability layer
    """

    def __init__(self, graph_router):
        self.bridge = BridgeV4(graph_router)
        self.ledger = ExecutionLedgerV1()

        self.replay_engine = ReplayEngineV1(
            bridge=self.bridge,
            ledger=self.ledger
        )

    def run(self, query: str):
        return self.bridge.run(query)

    def replay(self, query: str, plan: dict):
        return self.replay_engine.replay(query, plan)

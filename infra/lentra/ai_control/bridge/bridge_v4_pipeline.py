from lentra.ai_control.bridge.bridge_v4 import BridgeV4


class BridgeV4Pipeline:
    """
    Thin orchestration wrapper
    """

    def __init__(self, graph_router):
        self.bridge = BridgeV4(graph_router)

    def run(self, query: str):
        return self.bridge.run(query)

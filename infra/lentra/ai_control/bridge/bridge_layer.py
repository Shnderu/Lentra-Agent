from typing import Dict, Any


class BridgeLayer:
    """
    Minimal stable compatibility layer for BridgeV3/BridgeV4.
    DOES NOT contain business logic.
    Only normalizes GraphRouter output.
    """

    def __init__(self, graph_router):
        self.graph_router = graph_router

    def resolve(self, query: str) -> Dict[str, Any]:
        """
        Normalize routing output into execution-safe format.
        """

        route = self.graph_router.route(query)

        return {
            "query": query,
            "nodes": route.get("selected_node", []),
            "symbols": route.get("selected_symbols", []),
            "files": route.get("files", []),
            "expanded_files": route.get("expanded_files", route.get("files", [])),
        }

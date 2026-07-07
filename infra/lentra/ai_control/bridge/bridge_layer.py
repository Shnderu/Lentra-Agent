from typing import Dict, Any


class BridgeLayer:
    """
    Compatibility layer between GraphRouter and execution pipeline.

    Normalizes current GraphRouter output.
    Does not contain business logic.
    """

    def __init__(self, graph_router):
        self.graph_router = graph_router


    def resolve(
        self,
        query: str
    ) -> Dict[str, Any]:

        route = self.graph_router.route(query)

        return {
            "query": query,

            "nodes": route.get(
                "nodes",
                route.get("selected_node", [])
            ),

            "symbols": route.get(
                "symbols",
                route.get("selected_symbols", [])
            ),

            "files": route.get(
                "files",
                []
            ),

            "expanded_files": route.get(
                "expanded_files",
                route.get("files", [])
            ),

            "intent": route.get(
                "intent"
            ),

            "metadata": route.get(
                "metadata",
                {}
            ),
        }

from dataclasses import dataclass
from typing import List, Dict, Any

from lentra.ai_control.bridge.bridge_layer import BridgeLayer


@dataclass
class Plan:
    query: str
    files: List[str]
    expanded_files: List[str]
    nodes: List[str]
    symbols: List[str]


class BridgeV3:

    def __init__(self, graph_router, git_root="/opt/lentra", aider_executor=None):
        self.graph_router = graph_router
        self.git_root = git_root
        self.aider = aider_executor
        self.layer = BridgeLayer(graph_router)

    def build_plan(self, query: str) -> Plan:
        route = self.graph_router.route(query)

        files = route.get("files", [])
        expanded = route.get("expanded_files", files)

        return Plan(
            query=query,
            files=files,
            expanded_files=expanded,
            nodes=route.get("selected_node", []),
            symbols=route.get("selected_symbols", []),
        )

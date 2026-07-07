from dataclasses import dataclass
from typing import List

from lentra.ai_control.bridge.bridge_layer import BridgeLayer


@dataclass
class Plan:
    query: str
    files: List[str]
    expanded_files: List[str]
    nodes: List[str]
    symbols: List[str]


class BridgeV3:

    def __init__(
        self,
        graph_router,
        git_root="/opt/lentra",
        aider_executor=None
    ):
        self.git_root = git_root
        self.aider = aider_executor
        self.layer = BridgeLayer(graph_router)


    def build_plan(
        self,
        query: str
    ) -> Plan:

        route = self.layer.resolve(query)

        return Plan(
            query=query,
            files=route.get(
                "files",
                []
            ),
            expanded_files=route.get(
                "expanded_files",
                route.get("files", [])
            ),
            nodes=route.get(
                "nodes",
                []
            ),
            symbols=route.get(
                "symbols",
                []
            ),
        )

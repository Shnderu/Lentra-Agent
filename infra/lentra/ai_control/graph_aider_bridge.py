from __future__ import annotations

from typing import List, Dict, Any

from lentra.ai_control.aider_executor import AiderExecutor
from lentra.core.market_intelligence.graph_v2.router import GraphRouter
from lentra.core.market_intelligence.graph_v2.file_registry import GraphFileRegistry


class GraphAiderBridge:
    """
    Production bridge:

    GraphRouter → FileRegistry → AiderExecutor
    """

    def __init__(self):
        self.router = GraphRouter()
        self.registry = GraphFileRegistry()
        self.executor = AiderExecutor()

    def _nodes_to_files(self, nodes: List[str]) -> List[str]:
        files: List[str] = []

        for node in nodes:
            files.extend(self.registry.resolve(node))

        # dedupe stable
        seen = set()
        out = []
        for f in files:
            if f not in seen:
                seen.add(f)
                out.append(f)

        return out

    def run(self, instruction: str) -> Dict[str, Any]:
        route = self.router.route(instruction)

        nodes = route.get("selected_node", [])

        files = self._nodes_to_files(nodes)

        if not files:
            return {
                "status": "no_targets",
                "route": route,
                "files": [],
                "result": None
            }

        result = self.executor.full_cycle(instruction, files)

        return {
            "status": "ok",
            "route": route,
            "files": files,
            "result": result
        }

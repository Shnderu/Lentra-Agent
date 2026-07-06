from __future__ import annotations

from typing import Dict, Any, List, Optional

from lentra.core.market_intelligence.graph_v2.selector import GraphSelector


class GraphRouter:
    """
    Production routing layer for Graph V2.

    Responsibilities:
    - Convert query → graph selection
    - Use prebuilt index (NO repo scan)
    - Output execution plan for Market Intelligence pipeline
    """

    def __init__(self, index_path: Optional[str] = None):
        self.selector = GraphSelector(index_path=index_path)

    def route(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main routing entrypoint.

        Returns:
            {
                "query": str,
                "nodes": [...],
                "engines": [...],
                "confidence": float,
                "graph_version": "v2"
            }
        """
        context = context or {}

        selection = self.selector.select(query=query, context=context)

        nodes = selection.get("nodes", [])
        engines = selection.get("engines", [])
        confidence = selection.get("confidence", 0.0)

        return {
            "query": query,
            "nodes": nodes,
            "engines": engines,
            "confidence": confidence,
            "graph_version": "v2",
        }

    def route_batch(self, queries: List[str], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        context = context or []
        return [self.route(q, context) for q in queries]

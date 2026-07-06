from __future__ import annotations

from lentra.core.market_intelligence.graph_v2.build_index import build_graph_index
from lentra.core.market_intelligence.graph_v2.selector import GraphSelector


class GraphRouter:
    """
    Lightweight routing layer over graph selector.
    """

    def __init__(self):
        self.index = build_graph_index()
        self.selector = GraphSelector(self.index)

    def route(self, query: str):
        selected = self.selector.select(query)

        return {
            "query": query,
            "selected_node": selected,
        }

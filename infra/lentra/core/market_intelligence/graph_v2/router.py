from typing import Dict, Any

from lentra.core.market_intelligence.graph_v2.build_symbol_index import build_symbol_index


class GraphRouter:

    def __init__(self):
        self.index = build_symbol_index()

    def route(self, query: str) -> Dict[str, Any]:
        nodes = self._simple_match(query)

        symbols = []
        for n in nodes:
            entry = self.index.nodes.get(n)
            if entry:
                symbols.extend(entry.symbols)

        return {
            "query": query,
            "selected_node": nodes,
            "selected_symbols": list(set(symbols))
        }

    def _simple_match(self, query: str):
        q = query.lower()

        if "risk" in q:
            return ["risk_engine"]
        if "price" in q:
            return ["pricing_engine"]
        if "rank" in q:
            return ["ranking_engine"]
        if "studio" in q or "apartment" in q:
            return ["area_engine"]

        return []

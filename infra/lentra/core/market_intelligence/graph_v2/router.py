from lentra.core.market_intelligence.graph_v2.selector import GraphSelector
from lentra.core.market_intelligence.graph_v2.build_index import build_graph_index
from lentra.core.market_intelligence.graph_v2.signal_enricher import SignalEnricherV1


class GraphRouter:
    def __init__(self):
        self.index = build_graph_index()
        self.selector = GraphSelector(index=self.index)
        self.enricher = SignalEnricherV1()

    def _normalize_selector_output(self, base):
        """
        GraphSelector may return:
        - list[str]
        - dict
        Normalize into dict contract for downstream layers.
        """

        if base is None:
            return {}

        if isinstance(base, dict):
            return base

        if isinstance(base, list):
            return {
                "selected_node": base,
                "selected_symbols": [],
                "files": [],
            }

        return {
            "selected_node": [],
            "selected_symbols": [],
            "files": [],
        }

    def route(self, query: str):
        raw = self.selector.select(query)

        base = self._normalize_selector_output(raw)

        enriched = self.enricher.enrich(query, base)

        return {
            "query": query,
            "selected_node": enriched.nodes,
            "selected_symbols": enriched.symbols,
            "selected_files": enriched.files,
            "intent": enriched.intent,
        }

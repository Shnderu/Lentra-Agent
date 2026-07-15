from lentra.core.market_intelligence.graph_v2.graph_selector import GraphSelector
from lentra.core.market_intelligence.graph_v2.graph_index import GraphIndex
from lentra.core.market_intelligence.graph_v2.signal_enricher import SignalEnricher


class GraphRouter:
    """
    FULLY CONTRACT-ALIGNED ROUTER

    GraphV2 routing layer only.
    Does not import runtime engines.
    Does not execute intelligence modules.
    """

    def __init__(self):
        index = GraphIndex(
            nodes={
                "risk_engine": {},
                "dedup_engine": {},
                "area_engine": {},
            }
        )

        self.selector = GraphSelector(index)
        self.enricher = SignalEnricher()

    def route(self, query: str):
        base = self.selector.select(query)

        enriched = self.enricher.enrich(
            query,
            {
                "selected_node": base,
                "selected_symbols": self._symbols(base),
                "selected_files": self._files(base),
            },
        )

        return enriched

    def _symbols(self, nodes):
        mapping = {
            "risk_engine": [
                "RiskEngine",
                "RiskEngine.run",
            ],
            "dedup_engine": [
                "DedupEngine",
                "DedupEngine.run",
            ],
            "area_engine": [
                "AreaEngine",
                "AreaEngine.run",
            ],
        }

        out = []

        for node in nodes:
            out.extend(mapping.get(node, []))

        return out

    def _files(self, nodes):
        mapping = {
            "risk_engine": [
                "lentra/core/market_intelligence/engines/risk_engine.py",
            ],
            "dedup_engine": [
                "lentra/core/market_intelligence/engines/dedup_engine.py",
                "lentra/core/market_intelligence/dedup/dedup_engine.py",
            ],
            "area_engine": [
                "lentra/core/market_intelligence/area/area_engine.py",
            ],
        }

        out = []

        for node in nodes:
            out.extend(mapping.get(node, []))

        return out

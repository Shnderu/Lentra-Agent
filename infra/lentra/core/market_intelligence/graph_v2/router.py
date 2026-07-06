from lentra.core.market_intelligence.graph_v2.graph_selector import GraphSelector
from lentra.core.market_intelligence.graph_v2.graph_index import GraphIndex
from lentra.core.market_intelligence.graph_v2.signal_enricher import SignalEnricher


class GraphRouter:
    """
    FULLY CONTRACT-ALIGNED ROUTER
    """

    def __init__(self):
        index = GraphIndex(nodes={
            "risk_engine": {},
            "dedup_engine": {},
            "area_engine": {},
        })

        self.selector = GraphSelector(index)
        self.enricher = SignalEnricher()

    def route(self, query: str):
        base = self.selector.select(query)

        enriched = self.enricher.enrich(query, {
            "selected_node": base,
            "selected_symbols": self._symbols(base),
            "selected_files": self._files(base),
        })

        return enriched

    def _symbols(self, nodes):
        mapping = {
            "risk_engine": ["RiskModule", "RiskModule.run"],
            "dedup_engine": ["DedupEngine"],
            "area_engine": ["AreaEngine"],
        }

        out = []
        for n in nodes:
            out += mapping.get(n, [])
        return out

    def _files(self, nodes):
        mapping = {
            "risk_engine": ["infra/lentra/core/market_intelligence/risk/risk_engine.py"],
            "dedup_engine": ["infra/lentra/core/market_intelligence/dedup/dedup_engine.py"],
            "area_engine": ["infra/lentra/core/market_intelligence/area/area_engine.py"],
        }

        out = []
        for n in nodes:
            out += mapping.get(n, [])
        return out

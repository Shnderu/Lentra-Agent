from lentra.core.market_intelligence.graph_v2.selector import GraphSelector
from lentra.core.market_intelligence.graph_v2.signal_enricher import SignalEnricher


class GraphRouter:

    def __init__(self, index):
        self.selector = GraphSelector(index=index)
        self.enricher = SignalEnricher()

    def route(self, query: str):
        base = self.selector.select(query)

        enriched = self.enricher.enrich(query, base)

        return enriched

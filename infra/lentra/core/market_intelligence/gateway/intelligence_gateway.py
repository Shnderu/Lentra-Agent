from typing import Dict, Any

from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1


class IntelligenceGateway:
    """
    V2 Intelligence Gateway
    Single entrypoint for Market Intelligence OS
    """

    def __init__(self):
        self.signals_engine = SignalsEngineV1()
        self._enrichment = None

        # engine registry (replaces isolator concept)
        self._engines = {
            "signals": self.signals_engine,
            "enrichment": None  # lazy init
        }

    def get_engine_keys(self):
        return list(self._engines.keys())

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        # 1. Signals layer
        signals_result = self.signals_engine.build(payload)

        # 2. Enrichment layer (lazy)
        enrichment = self._get_enrichment()
        enriched = enrichment.compute(signals_result)

        return {
            **signals_result,
            "enrichment": enriched
        }

    def _get_enrichment(self):
        if self._enrichment is None:
            from lentra.core.market_intelligence.enrichment.enrichment_layer import EnrichmentLayer
            self._enrichment = EnrichmentLayer()

        return self._enrichment

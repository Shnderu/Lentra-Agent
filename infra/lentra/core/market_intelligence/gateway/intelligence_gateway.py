from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1


class IntelligenceGateway:

    def __init__(self):
        self.signals_engine = SignalsEngineV1()
        self._enrichment = None

    def _get_enrichment(self):
        if self._enrichment is None:
            from lentra.core.market_intelligence.enrichment.enrichment_layer import EnrichmentLayer
            self._enrichment = EnrichmentLayer()
        return self._enrichment

    def compute(self, payload: dict):

        base_result = self.signals_engine.compute(payload)

        try:
            enrichment = self._get_enrichment()
            return enrichment.compute(base_result)
        except Exception:
            # CRITICAL: NEVER break API
            return base_result

# PATCH SNIPPET (apply manually or via merge tool)

from lentra.core.market_intelligence.enrichment.enrichment_layer import EnrichmentLayer


class IntelligenceGatewayEnrichmentMixin:
    def __init__(self):
        self.enrichment = EnrichmentLayer()

    def enrich(self, engine_result: dict) -> dict:
        enrichment = self.enrichment.compute(engine_result)

        return {
            **engine_result,
            "enrichment": enrichment
        }

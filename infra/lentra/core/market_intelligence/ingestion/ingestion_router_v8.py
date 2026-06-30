from lentra.services.intelligence_gateway import IntelligenceGateway


class IngestionRouterV8:

    def __init__(self):
        self.gateway = IntelligenceGateway()

    def route(self, enriched_listings):
        return self.gateway.execute(enriched_listings, source="ingestion")

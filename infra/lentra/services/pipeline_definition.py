from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine


class Pipeline:

    def __init__(self):
        self.intel = MarketIntelligenceEngine()

    def execute(self, payload: dict):

        # 🔧 FIX: ensure query propagation
        query = payload.get("query", "")

        property_object = {
            "query": query,
            "listings": payload.get("listings", [])
        }

        intelligence = self.intel.analyze(property_object)

        return {
            "intelligence": intelligence
        }


pipeline = Pipeline()

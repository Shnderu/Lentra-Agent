from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine


class PipelineDefinition:

    def __init__(self):
        self.intel = MarketIntelligenceEngine()

    def run(self, listings):
        return self.intel.analyze({
            "task": "pipeline",
            "listings": listings
        })

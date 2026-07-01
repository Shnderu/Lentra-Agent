from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

class IntelligenceAdapter:

    def __init__(self):
        self.engine = MarketIntelligenceEngine()

    def analyze(self, listings: list) -> dict:
        return self.engine.analyze({
            "task": "batch_analysis",
            "listings": listings
        })

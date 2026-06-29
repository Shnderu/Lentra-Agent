from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine


class IntelligenceAdapter:

    def __init__(self):
        self.engine = MarketIntelligenceEngine()

    def analyze(self, listings: list) -> list:
        return self.engine.analyze(listings)

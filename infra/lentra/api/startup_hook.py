from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

# SINGLE CANONICAL ENGINE WRAPPER
engine = MarketIntelligenceEngine()


def get_engine():
    return engine

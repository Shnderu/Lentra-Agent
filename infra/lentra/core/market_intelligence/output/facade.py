from typing import Any, Dict

from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine


class MarketIntelligenceOutputFacade:
    """
    SINGLE ENTRY POINT FOR ALL SYSTEMS

    API / BOT / WORKER / RUNTIME → ONLY HERE
    """

    def __init__(self):
        self.engine = MarketIntelligenceEngine()

    def analyze(self, payload: Dict[str, Any]):
        return self.engine.analyze(payload)

    def interpret(self, payload: Dict[str, Any]):
        return self.engine.analyze(payload)

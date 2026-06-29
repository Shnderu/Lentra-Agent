from typing import Dict, Any

from lentra.services.market_intelligence_v2 import MarketIntelligenceV2
from lentra.services.price_engine import PriceEngine
from lentra.services.dedup_engine import DedupEngine
from lentra.services.risk_engine import RiskEngine


class MarketIntelligenceOrchestrator:

    def __init__(self):
        self.market = MarketIntelligenceV2()
        self.price = PriceEngine()
        self.dedup = DedupEngine()
        self.risk = RiskEngine()

    def analyze(self, intent: Dict[str, Any]) -> Dict[str, Any]:

        query = intent.get("query", "")

        market = self.market.analyze(intent)
        price = self.price.evaluate(intent, market)
        dedup = self.dedup.cluster(intent, market, price)
        risk = self.risk.score(intent, market, price, dedup)

        return {
            "version": "v2_orchestrated",
            "query": query,
            "market": market,
            "price": price,
            "dedup": dedup,
            "risk": risk
        }

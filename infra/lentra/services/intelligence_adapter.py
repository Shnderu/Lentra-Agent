from typing import Dict, Any

from .intelligence import intelligence_service
from .market_scoring_engine import MarketScoringEngine


class MarketIntelligence:
    """
    Adapter = orchestration only
    """

    def __init__(self):
        self.scorer = MarketScoringEngine()

    def analyze(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        query = intent.get("query", "")

        signals = intelligence_service.analyze(query, intent)

        return self.scorer.build_market(signals["signals"])

    def price_check(self, intent, market):
        return self.scorer.price_check(market, intent.get("budget_max"))

    def risk_score(self, intent, market):
        return self.scorer.risk(market)

    def dedup(self, intent, market):
        return self.scorer.dedup(intent)

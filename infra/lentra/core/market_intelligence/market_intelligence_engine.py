from typing import Any, Dict

from lentra.core.market_intelligence.layers.pricing.engine import PricingLayer
from lentra.core.market_intelligence.layers.risk.engine import RiskLayer
from lentra.core.market_intelligence.layers.dedup.engine import DedupLayer
from lentra.core.market_intelligence.layers.area.engine import AreaLayer


class MarketIntelligenceEngine:
    """
    Canonical deterministic pipeline engine.
    No routing logic. No hidden decision trees.
    """

    def __init__(self):
        self.pricing = PricingLayer()
        self.risk = RiskLayer()
        self.dedup = DedupLayer()
        self.area = AreaLayer()

    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        enriched = payload

        enriched = self.dedup.process(enriched)
        enriched = self.pricing.process(enriched)
        enriched = self.risk.process(enriched)
        enriched = self.area.process(enriched)

        return {
            "input": payload,
            "result": enriched,
            "verdict": self._verdict(enriched)
        }

    def _verdict(self, enriched: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "ok",
            "confidence": enriched.get("confidence", 0.5),
            "type": "market_intelligence"
        }

from typing import Dict, Any
from lentra.core.engines.base_engine import BaseEngine


class MarketIntelligenceEngine(BaseEngine):
    """
    Minimal working version (Phase 1 compatible)
    """

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        price = ctx.get("price", 0)
        market_price = ctx.get("market_price", 1)

        deviation = abs(price - market_price) / max(market_price, 1)

        return {
            "pricing_score": max(0.0, 1.0 - deviation),
            "direction": "over" if price > market_price else "under",
            "deviation": deviation,
            "confidence": 0.9,
            "version": "pricing_v2_fixed"
        }

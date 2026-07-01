from typing import Dict, Any, Optional


class PricingEngine:
    """
    Contract-stable pricing engine.
    Never receives raw positional dependencies.
    """

    def evaluate(self, payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}

        market_stats = context.get("market_stats", {})

        return self.score(payload, market_stats)

    def score(self, payload: Dict[str, Any], market_stats: Dict[str, Any]) -> Dict[str, Any]:
        price = payload.get("price", 0)

        market_price = market_stats.get("market_price", price) if market_stats else price

        deviation = 0.0
        if market_price:
            deviation = abs(price - market_price) / market_price * 100

        return {
            "price": price,
            "market_price": market_price,
            "deviation_pct": round(deviation, 2),
            "signal": "hold"
        }

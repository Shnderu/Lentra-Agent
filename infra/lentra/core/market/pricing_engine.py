from typing import Dict, Any, Optional


class PricingEngine:
    """
    Contract-stable pricing engine (ARCH V2)
    """

    def evaluate(self, payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return self.score(payload, context)

    def score(self, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        price = payload.get("price", 0)

        market_price = payload.get("market_price")
        if market_price is None:
            raise ValueError("market_price is REQUIRED in ARCH V2 contract")

        deviation = 0.0
        if market_price:
            deviation = abs(price - market_price) / market_price * 100

        signal = "hold"
        if deviation > 20:
            signal = "risk"
        elif deviation > 10:
            signal = "hold"
        else:
            signal = "buy"

        return {
            "price": price,
            "market_price": market_price,
            "deviation_pct": round(deviation, 2),
            "signal": signal
        }

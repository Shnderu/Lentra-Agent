from typing import Dict, Any


class PricingProvider:
    """
    SAFE STUB (bootstrap fix)

    PURPOSE:
    - ensure engine import stability
    - restore API boot
    - logic will be re-attached later
    """

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("price", 0)
        market = data.get("market_price", 1)

        deviation = abs(price - market) / market if market else 0

        return {
            "score": 1 - deviation,
            "direction": "over" if price > market else "under",
            "deviation": round(deviation, 4),
            "confidence": 1 - deviation
        }

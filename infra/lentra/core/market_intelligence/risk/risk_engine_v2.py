from typing import Dict, Any, Optional


class RiskEngineV2:
    """
    Unified risk engine (contract aligned with pricing engine).
    """

    def evaluate(self, payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return self.process(payload)

    def process(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        risk = listing.get("risk", 0.5)

        price = listing.get("price", 0)
        market_price = listing.get("market_price", price)

        deviation = abs(price - market_price) / max(market_price or 1, 1)

        listing["risk"] = min(1.0, risk + deviation * 0.3)
        listing["deviation_pct"] = deviation * 100

        return {
            "risk_level": listing["risk"],
            "deviation_pct": listing["deviation_pct"],
            "raw": listing
        }

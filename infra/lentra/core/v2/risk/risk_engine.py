from typing import Dict, Any, List


class RiskEngineV2:

    def score(self, listing: Dict[str, Any], market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        v2 risk scoring:
        - deviation from market
        - missing fields
        - suspicious pricing patterns
        """

        risk = 0
        flags: List[str] = []

        price = listing.get("price")
        market_price = market_context.get("market_price")

        if price is None:
            risk += 60
            flags.append("no_price")

        if market_price and price:
            deviation = ((price - market_price) / market_price) * 100

            if abs(deviation) > 30:
                risk += 30
                flags.append("high_deviation")

            if price < market_price * 0.5:
                risk += 40
                flags.append("too_cheap")

        if not listing.get("description"):
            risk += 10
            flags.append("no_description")

        return {
            "risk_score": min(risk, 100),
            "flags": flags,
            "level": (
                "low" if risk < 30 else
                "medium" if risk < 70 else
                "high"
            ),
            "deviation": deviation if market_price and price else None
        }

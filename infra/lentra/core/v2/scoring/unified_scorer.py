from typing import Dict, Any


class UnifiedScorerV2:

    def score(self, listing: Dict[str, Any], market: Dict[str, Any]) -> Dict[str, Any]:
        """
        Финальный слой интерпретации объекта
        """

        base = 100

        price = listing.get("price") or 0

        # --- MARKET SIGNAL ---
        market_price = market.get("market_price")

        if market_price and price:
            deviation = abs(price - market_price) / market_price * 100

            if deviation < 10:
                base += 10
            elif deviation < 25:
                base -= 5
            else:
                base -= 20

        # --- RISK SIGNAL ---
        risk = listing.get("risk_score", 0)
        base -= risk * 0.9

        # --- AREA SIGNAL ---
        area = (listing.get("area_v2") or {}).get("area_score")

        if area:
            if area >= 8:
                base += 10
            elif area >= 6:
                base += 3
            else:
                base -= 8

        # clamp
        base = max(0, min(100, base))

        return {
            "score": round(base, 2),
            "verdict": self._verdict(base)
        }

    def _verdict(self, score: float) -> str:
        if score >= 80:
            return "excellent_deal"
        if score >= 65:
            return "good_deal"
        if score >= 45:
            return "neutral"
        return "risky"

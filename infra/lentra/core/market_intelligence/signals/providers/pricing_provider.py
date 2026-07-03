from typing import Dict, Any


class PricingSignalProvider:
    """
    Pricing Signal V2

    Adds:
    - asymmetry awareness
    - market band logic
    - anomaly detection
    """

    name = "pricing"

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("price", 0)
        market = data.get("market_price", 0)

        if not market or market <= 0:
            return {
                "score": 0.0,
                "direction": "unknown",
                "deviation": 0.0,
                "band": "unknown"
            }

        deviation = (price - market) / market

        abs_dev = abs(deviation)

        # -----------------------------
        # BAND MODEL (market positioning)
        # -----------------------------
        if abs_dev < 0.05:
            band = "market_fair"
            score = 0.2
        elif abs_dev < 0.15:
            band = "slight_deviation"
            score = 0.5
        elif abs_dev < 0.30:
            band = "significant_deviation"
            score = 0.8
        else:
            band = "outlier"
            score = 1.0

        # -----------------------------
        # ASYMMETRY PENALTY
        # -----------------------------
        # переплата хуже недооценки
        if deviation > 0:
            score *= 1.15  # overpay penalty boost
            direction = "over"
        else:
            score *= 0.9   # underprice less critical
            direction = "under"

        # clamp
        score = min(max(score, 0.0), 1.0)

        # -----------------------------
        # FINAL SIGNAL
        # -----------------------------
        return {
            "score": round(score, 4),
            "direction": direction,
            "deviation": round(deviation, 6),
            "band": band,
            "market_price": market
        }

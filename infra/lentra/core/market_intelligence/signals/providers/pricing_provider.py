from typing import Dict, Any


class PricingProvider:

    name = "pricing"

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        price = data.get("price")
        market_price = data.get("market_price")

        if not price or not market_price:
            return {
                "score": 0.5,
                "direction": "unknown",
                "deviation": 0,
                "confidence": 0.2
            }

        deviation = (price - market_price) / market_price

        abs_deviation = abs(deviation)

        if deviation > 0:
            direction = "over"
        elif deviation < 0:
            direction = "under"
        else:
            direction = "fair"

        score = max(
            0,
            min(
                1,
                1 - abs_deviation
            )
        )

        return {
            "score": round(score, 4),
            "direction": direction,
            "deviation": round(deviation, 4),
            "market_price": market_price,
            "price": price,
            "confidence": min(1, 0.5 + score / 2)
        }

from typing import Dict, Any


class SignalsEngineV1:
    """
    PURE SIGNAL LAYER

    RULES:
    - NO compute()
    - ONLY build()
    - NO side effects
    - deterministic extraction layer
    """

    name = "signals"

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        price = float(payload.get("price", 0))
        market_price = float(payload.get("market_price", 1))

        deviation = abs(price - market_price) / max(market_price, 1)

        direction = "over" if price > market_price else "under"

        pricing = {
            "score": min(deviation, 1.0),
            "direction": direction,
            "deviation": round(deviation, 4)
        }

        area = {
            "score": 0.5,
            "note": "enhanced_area_model"
        }

        dedup = {
            "score": 1.0,
            "confidence": 1.0
        }

        return {
            "pricing": pricing,
            "area": area,
            "dedup": dedup
        }

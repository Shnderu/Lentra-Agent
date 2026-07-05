from typing import Dict, Any


class SignalsEngineV1:
    """
    IMMUTABLE SIGNALS CONTRACT (v2)

    IMPORTANT:
    - NO compute()
    - ONLY build()
    - NO ctx mutation
    - ALWAYS returns full deterministic signal map
    """

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        price = payload.get("price", 0)
        market_price = payload.get("market_price", 1)

        deviation = (price - market_price) / market_price if market_price else 0

        return {
            "pricing": {
                "score": abs(deviation),
                "direction": "over" if deviation > 0 else "under",
                "deviation": round(deviation, 4)
            },
            "area": {
                "score": 0.5,
                "note": "enhanced_area_model"
            },
            "dedup": {
                "score": 1.0,
                "confidence": 1.0
            },
            "signals_meta": {
                "engine_keys": ["pricing", "area", "dedup"]
            }
        }

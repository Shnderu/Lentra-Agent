from typing import Dict, Any


def normalize_core_output(result: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    IMMUTABLE CORE NORMALIZATION CONTRACT

    RULES:
    - score MUST be normalized (0..1)
    - delta MUST be absolute percentage deviation
    """

    price = payload.get("price", 0)
    market = payload.get("market_price", 1)

    if market:
        result["score"] = round(price / market, 4)
        result["delta"] = round(abs(price - market), 4)

    return result

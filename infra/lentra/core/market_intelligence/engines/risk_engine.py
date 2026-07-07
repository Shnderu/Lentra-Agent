from typing import Dict, Any


class RiskEngine:
    """
    V3 SAFE CONTRACT

    input:
        accumulated result dict

    output:
        enriched result dict
    """

    def evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        price = result.get("price", 0)
        market = result.get("market_price", 0)

        if market:
            deviation = abs(price - market) / market
        else:
            deviation = 0

        if deviation <= 0.05:
            level = "low"
        elif deviation <= 0.20:
            level = "medium"
        else:
            level = "high"

        result["risk"] = {
            "delta": round(deviation, 4),
            "level": level,
            "status": "ok"
        }

        return result

from typing import Dict, Any

class RiskLayer:
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(payload)

        base_risk = 0.5

        if payload.get("duplicates", 0) > 2:
            base_risk += 0.2

        if payload.get("price", 0) > payload.get("market_price", 0):
            base_risk += 0.1

        payload["risk"] = {
            "score": min(base_risk, 1.0),
            "level": "high" if base_risk > 0.7 else "medium"
        }

        return payload

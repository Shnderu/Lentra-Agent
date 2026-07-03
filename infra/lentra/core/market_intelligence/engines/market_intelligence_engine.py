from typing import Dict, Any


class MarketIntelligenceEngine:
    """
    Canonical aggregation engine (MVP safe version)
    """

    def __init__(self, components: Dict[str, Any]):
        self.components = components or {}

    def fetch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return payload

    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    def dedup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["dedup"] = {"score": 1.0}
        return data

    def rank(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["ranking"] = {"score": 0.7}
        return data

    def risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("price", 0)
        market = data.get("market_price", 1)

        deviation = abs(price - market) / max(market, 1)

        data["risk"] = {
            "risk_level": min(deviation * 2, 1.0)
        }

        return data

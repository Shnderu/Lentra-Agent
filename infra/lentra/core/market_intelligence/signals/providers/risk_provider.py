from typing import Dict, Any


class RiskSignalProvider:
    """
    Risk Engine V2

    now includes:
    - price anomaly
    - completeness heuristic
    - duplication penalty
    - area context (NEW)
    """

    name = "risk"

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        price_risk = self._price_risk(data)
        completeness = self._completeness(data)
        duplication = self._duplication(data)
        heuristic = self._heuristic(data)
        area_factor = self._area_factor(data)

        # weighted v2 model
        score = (
            price_risk * 0.45 +
            completeness * 0.15 +
            duplication * 0.15 +
            heuristic * 0.10 +
            area_factor * 0.15
        )

        return {
            "score": round(score, 4),
            "risk_level": round(score, 4),
            "level": self._level(score),
            "components": {
                "price_risk": round(price_risk, 4),
                "completeness": round(completeness, 4),
                "duplication": round(duplication, 4),
                "heuristic": round(heuristic, 4),
                "area_factor": round(area_factor, 4),
            }
        }

    def _price_risk(self, data: Dict[str, Any]) -> float:
        price = data.get("price", 0)
        market = data.get("market_price", 0)

        if not market:
            return 0.0

        deviation = abs(price - market) / market
        return min(deviation, 1.0)

    def _completeness(self, data: Dict[str, Any]) -> float:
        required = ["price", "market_price", "query"]
        missing = sum(1 for k in required if not data.get(k))
        return missing / len(required)

    def _duplication(self, data: Dict[str, Any]) -> float:
        return 1.0 - data.get("dedup", {}).get("score", 1.0)

    def _heuristic(self, data: Dict[str, Any]) -> float:
        # placeholder anti-scam heuristics
        query = (data.get("query") or "").lower()

        score = 0.0

        if "urgent" in query:
            score += 0.3
        if "cheap" in query:
            score += 0.2

        return min(score, 1.0)

    def _area_factor(self, data: Dict[str, Any]) -> float:
        area = data.get("area", {})

        if not area:
            return 0.3  # default uncertainty penalty

        # expat attractiveness inverse risk signal
        liquidity = area.get("components", {}).get("liquidity", 0.5)
        expat_intent = area.get("components", {}).get("expat_intent", 0.5)

        return 1.0 - ((liquidity + expat_intent) / 2)

    def _level(self, score: float) -> str:
        if score > 0.7:
            return "high"
        if score > 0.3:
            return "medium"
        return "low"

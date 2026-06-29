from typing import Dict, Any


class RiskEngine:
    def evaluate(self, property_obj: Dict[str, Any], market: Dict[str, Any]) -> Dict[str, Any]:
        raw = (property_obj.get("raw_query") or "").lower()
        location = property_obj.get("location") or ""

        risk = 0

        # heuristic signals
        if "cheap" in raw:
            risk += 1

        if "beach" in raw and location in ["da nang", "bali"]:
            risk += 1

        if property_obj.get("budget_max", 0) < 300:
            risk += 2

        # location signal
        if location == "unknown" or not location:
            risk += 2

        if risk <= 1:
            level = "low"
        elif risk <= 3:
            level = "medium"
        else:
            level = "high"

        return {
            "risk_score": risk,
            "risk_level": level,
            "reasons": self._explain(risk, raw, location)
        }

    def _explain(self, risk: int, raw: str, location: str):
        reasons = []

        if "cheap" in raw:
            reasons.append("price_above_market_signal_missing")

        if not location:
            reasons.append("missing_location_context")

        if risk >= 3:
            reasons.append("multi_signal_risk")

        return reasons


risk_engine = RiskEngine()

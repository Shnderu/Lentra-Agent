from typing import Dict, Any


class RiskEngine:
    def evaluate(self, property_obj: Dict[str, Any], market: Dict[str, Any] = None) -> Dict[str, Any]:
        market = market or {}

        budget = property_obj.get("budget_max")

        # HARD NORMALIZATION (critical fix)
        if budget is None:
            budget = 0

        try:
            budget = float(budget)
        except Exception:
            budget = 0

        risk_score = 0.2

        if budget < 300:
            risk_score += 0.3

        if market.get("risk_level") == "unknown":
            risk_score += 0.2

        risk_score = min(risk_score, 1.0)

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": "low" if risk_score < 0.5 else "medium",
        }


risk_engine = RiskEngine()

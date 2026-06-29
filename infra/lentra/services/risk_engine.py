from typing import Dict, Any, List


class RiskEngine:
    def evaluate(self, property_obj: Dict[str, Any], market: Dict[str, Any] = None) -> Dict[str, Any]:
        market = market or {}

        # ---- SAFE BUDGET NORMALIZATION ----
        budget_raw = property_obj.get("budget_max", 0)

        try:
            budget = int(budget_raw) if budget_raw is not None else 0
        except Exception:
            budget = 0

        # ---- MARKET SIGNALS ----
        price_band = market.get("price_band") or {"min": 200, "max": 500}

        try:
            avg_price = (price_band.get("min", 0) + price_band.get("max", 0)) / 2
        except Exception:
            avg_price = 0

        # ---- RISK LOGIC ----
        reasons: List[str] = []

        risk_score = 0.0

        if budget <= 0:
            risk_score += 0.3
            reasons.append("missing_budget_signal")

        if avg_price > 0 and budget > 0:
            deviation = (avg_price - budget) / budget
        else:
            deviation = 0

        # price mismatch risk
        if deviation > 0.2:
            risk_score += 0.4
            reasons.append("price_above_budget_threshold")
        elif deviation < -0.3:
            risk_score += 0.1
            reasons.append("price_below_market_possible_outlier")

        # clamp
        risk_score = max(0.0, min(1.0, risk_score))

        if risk_score < 0.3:
            risk_level = "low"
        elif risk_score < 0.7:
            risk_level = "medium"
        else:
            risk_level = "high"

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "reasons": reasons
        }


# stable singleton (DO NOT BREAK OLD IMPORTS)
risk_engine = RiskEngine()

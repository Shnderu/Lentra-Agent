from typing import Dict, Any


class SignalConsistency:

    @staticmethod
    def evaluate(
        risk: Dict[str, Any],
        expat: Dict[str, Any],
        price: float,
        market_price: float
    ) -> Dict[str, Any]:

        conflicts = []
        adjustment = 0.0

        risk_level = risk.get("risk_level", "unknown")
        area_score = expat.get("area_score", 0.0)

        deviation = ((price - market_price) / market_price * 100) if market_price else 0.0

        # rule 1: high risk but strong buy signal tension
        if risk_level == "high" and deviation < -5:
            conflicts.append("risk_price_conflict")
            adjustment -= 0.1

        # rule 2: high area score should reduce risk impact
        if area_score > 0.7 and risk_level == "high":
            adjustment += 0.05

        # rule 3: overpriced + bad area
        if deviation > 10 and area_score < 0.3:
            conflicts.append("overprice_low_area")
            adjustment -= 0.08

        return {
            "conflicts": conflicts,
            "confidence_adjustment": adjustment,
            "consistency_score": max(0.0, 1.0 - len(conflicts) * 0.1)
        }

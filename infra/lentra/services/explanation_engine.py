from typing import Dict, Any


class ExplanationEngine:
    """
    v1: converts intelligence verdict into human + actionable reasoning
    """

    def build(self, analysis: Dict[str, Any], verdict: Dict[str, Any]) -> Dict[str, Any]:
        price = analysis.get("market_price_estimate")
        deviation = analysis.get("price_deviation_pct")
        location = analysis.get("location", "unknown")

        reasons = []

        if deviation is not None:
            if deviation > 10:
                reasons.append("Price is above market average for this area")
            elif deviation < -10:
                reasons.append("Price is below market average (possible deal or risk)")

        if analysis.get("risk_score", 0) > 0.5:
            reasons.append("Listing has elevated risk signals")

        recommendations = []

        if verdict.get("verdict") == "OVERPRICED":
            recommendations.append("Negotiate price or find alternatives nearby")
            recommendations.append("Check similar listings in same district")

        elif verdict.get("verdict") == "UNDERVALUED":
            recommendations.append("Act quickly — possible undervalued listing")
            recommendations.append("Verify legitimacy before payment")

        else:
            recommendations.append("Standard market offer")
            recommendations.append("Compare 2-3 alternatives before decision")

        return {
            "reasons": reasons,
            "recommendations": recommendations,
            "market_context": {
                "location": location,
                "market_price": price
            }
        }


explanation_engine = ExplanationEngine()

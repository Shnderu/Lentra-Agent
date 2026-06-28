

class AIDecisionEngine:

    def decide(self, market_analysis: dict, area_score: dict):

        risk = market_analysis.get("risk", 0.5)
        price_dev = market_analysis.get("price_deviation", 0)

        area = area_score.get("area_score", 5)

        # verdict logic
        if risk > 0.75:
            verdict = "high_risk"
        elif price_dev > 0.25:
            verdict = "overpriced"
        elif area > 8 and risk < 0.6:
            verdict = "strong_buy"
        else:
            verdict = "neutral"

        # negotiation logic
        if price_dev > 0.2:
            negotiation = "aggressive_offer"
            target_discount = 0.1
        else:
            negotiation = "low_room_for_negotiation"
            target_discount = 0.03

        # explanation layer
        explanation = [
            f"risk={risk:.2f}",
            f"price_deviation={price_dev:.2f}",
            f"area_score={area:.1f}"
        ]

        warnings = []

        if risk > 0.7:
            warnings.append("possible_fake_or_overpriced")

        if area < 6:
            warnings.append("weak_location")

        return {
            "verdict": verdict,
            "negotiation_strategy": negotiation,
            "target_discount": target_discount,
            "explanation": explanation,
            "warnings": warnings
        }

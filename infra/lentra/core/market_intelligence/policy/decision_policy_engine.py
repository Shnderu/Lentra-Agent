from typing import Dict, Any


class DecisionPolicyEngine:
    """
    Decision Policy Engine v1

    PURPOSE:
    - extract decision logic OUT of MarketIntelligenceEngine
    - make decision layer replaceable (A/B testing ready)
    - keep engine purely signal-based
    """

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})
        ranking = data.get("ranking", {})
        risk = data.get("risk", {})

        # ------------------------
        # INPUTS
        # ------------------------
        pricing_score = signals.get("pricing", {}).get("score", 0.0)
        area_score = signals.get("area", {}).get("score", 0.5)
        coupling_score = signals.get("coupling", {}).get("score", 0.0)
        risk_level = risk.get("risk_level", 0.0)

        ranking_score = ranking.get("score", 0.0)

        # ------------------------
        # CORE DECISION MODEL v1
        # ------------------------

        # weighted market score
        market_score = (
            pricing_score * 0.45 +
            area_score * 0.25 +
            coupling_score * 0.20 +
            ranking_score * 0.10
        )

        # risk penalty
        adjusted_score = market_score - (risk_level * 0.6)

        # ------------------------
        # DECISION RULES
        # ------------------------
        if adjusted_score >= 0.75:
            decision = "BUY"
        elif adjusted_score >= 0.55:
            decision = "HOLD"
        else:
            decision = "AVOID"

        # ------------------------
        # CONFIDENCE MODEL
        # ------------------------
        confidence = min(
            1.0,
            (pricing_score + area_score + coupling_score) / 3.0
        )

        return {
            "decision": decision,
            "final_score": round(adjusted_score, 4),
            "confidence": round(confidence, 4),
            "explanation": {
                "pricing": pricing_score,
                "area": area_score,
                "coupling": coupling_score,
                "risk": risk_level,
                "ranking": ranking_score,
                "market_score": round(market_score, 4),
                "adjusted_score": round(adjusted_score, 4)
            }
        }

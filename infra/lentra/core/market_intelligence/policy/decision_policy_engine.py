from typing import Dict, Any


class DecisionPolicyEngine:
    """
    v2 POLICY:
    включает:
    - ranking
    - coupling
    - risk
    - expat_score (НОВЫЙ СИЛЬНЫЙ ФАКТОР)
    """

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})
        ranking = data.get("ranking", {})
        risk = data.get("risk", {})

        expat = signals.get("expat", {}) or {}
        expat_score = expat.get("score", 0.5)

        # ------------------------
        # BASE INPUTS
        # ------------------------
        ranking_score = ranking.get("score", 0.5)
        risk_level = risk.get("risk_level", 0.5)

        coupling = signals.get("coupling", {})
        coupling_score = coupling.get("score", 0.5)

        # ------------------------
        # EXPAT BOOST LAYER (NEW REAL SIGNAL)
        # ------------------------
        # логика:
        # expat усиливает BUY если рынок "живой"
        # и снижает если район слабый

        expat_boost = (expat_score - 0.5) * 0.3

        # ------------------------
        # FINAL SCORE
        # ------------------------
        final_score = (
            ranking_score * 0.40 +
            coupling_score * 0.25 +
            (1 - risk_level) * 0.25 +
            expat_boost
        )

        final_score = max(0.0, min(1.0, final_score))

        # ------------------------
        # DECISION RULES
        # ------------------------
        if final_score >= 0.75:
            decision = "BUY"
        elif final_score >= 0.55:
            decision = "HOLD"
        else:
            decision = "AVOID"

        confidence = min(
            ranking_score,
            (1 - risk_level),
            max(0.5, expat_score)
        )

        return {
            "decision": decision,
            "final_score": round(final_score, 4),
            "confidence": round(confidence, 4),
            "explanation": {
                "ranking": ranking_score,
                "coupling": coupling_score,
                "risk": risk_level,
                "expat": expat_score,
                "expat_boost": round(expat_boost, 4)
            }
        }

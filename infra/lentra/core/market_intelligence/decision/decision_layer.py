from typing import Dict, Any


class DecisionLayer:
    """
    Decision Layer v1.0

    PRINCIPLE:
    - NO signal computation
    - NO duplication of engine logic
    - ONLY aggregation + final decision
    """

    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})
        ranking = data.get("ranking", {})
        risk = data.get("risk", {})

        pricing = signals.get("pricing", {}).get("score", 0.5)
        area = signals.get("area", {}).get("score", 0.5)
        coupling = signals.get("coupling", {}).get("score", 0.5)
        risk_score = risk.get("risk_level", 0.5)

        # =========================
        # DECISION WEIGHT MODEL v1
        # =========================

        decision_score = (
            pricing * 0.35 +
            area * 0.25 +
            coupling * 0.20 +
            (1 - risk_score) * 0.20
        )

        # normalize ranking fallback
        ranking_score = ranking.get("score", decision_score)

        final_score = 0.6 * ranking_score + 0.4 * decision_score

        # =========================
        # POLICY OUTPUT
        # =========================

        if final_score >= 0.75:
            decision = "ACCEPT"
        elif final_score >= 0.55:
            decision = "REVIEW"
        else:
            decision = "REJECT"

        return {
            "decision": decision,
            "decision_score": round(final_score, 4),
            "components": {
                "ranking": ranking_score,
                "decision": decision_score,
                "risk": risk_score
            },
            "signals": signals,
            "risk": risk,
            "ranking": ranking
        }

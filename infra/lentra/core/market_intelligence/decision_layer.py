from typing import Dict, Any


class DecisionLayer:

    def __init__(self):
        pass

    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Any]:

        ranking = data.get("ranking", {}).get("score", 0)
        risk = data.get("risk", {}).get("risk_level", 0)
        coupling = data.get("signals", {}).get("coupling", {}).get("score", 0)

        pricing_conf = data.get("signals", {}).get("pricing", {}).get("confidence", 0.5)

        # -----------------------
        # FINAL SCORE FUSION
        # -----------------------
        final_score = (
            ranking * 0.45 +
            coupling * 0.25 +
            (1 - risk) * 0.30
        )

        # -----------------------
        # DECISION ENGINE
        # -----------------------
        if final_score >= 0.75:
            decision = "BUY"
        elif final_score >= 0.55:
            decision = "HOLD"
        else:
            decision = "AVOID"

        # -----------------------
        # CONFIDENCE GATING
        # -----------------------
        confidence = min(pricing_conf, 1 - risk)

        # -----------------------
        # EXPLANATION TREE
        # -----------------------
        explanation = {
            "ranking_contribution": ranking * 0.45,
            "coupling_contribution": coupling * 0.25,
            "risk_penalty": risk * 0.30,
            "final_score": final_score
        }

        return {
            "decision": decision,
            "final_score": round(final_score, 4),
            "confidence": round(confidence, 4),
            "explanation": explanation
        }

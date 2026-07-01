from typing import Dict, Any


class SignalAuthorityGovernorV2:

    def arbitrate(self, meta: Dict[str, Any]) -> Dict[str, Any]:

        confidence = meta.get("confidence", 0.7)

        regime = meta.get("regime", {}).get("regime", "unknown")
        drift = meta.get("drift", {}).get("drift_score", 0.0)
        learning = meta.get("learning", {})
        feedback = meta.get("feedback", {})

        learning_boost = learning.get("confidence_tuning", 0.0)
        bias = learning.get("bias_shift", 0.0)

        feedback_bias = feedback.get("bias_correction", 0.0)

        # -------------------------
        # BASE WEIGHTS
        # -------------------------
        weights = {
            "authority": 1.0,
            "regime": 1.0,
            "learning": 1.0,
            "drift": 1.0,
            "feedback": 1.0,
        }

        # -------------------------
        # REGIME MODULATION
        # -------------------------
        if regime == "volatile":
            weights["authority"] *= 1.3
            weights["learning"] *= 0.8

        elif regime == "bull":
            weights["learning"] *= 1.2
            weights["authority"] *= 0.9

        elif regime == "bear":
            weights["authority"] *= 1.2
            weights["learning"] *= 0.9

        # -------------------------
        # DRIFT PENALTY
        # -------------------------
        if drift > 0.1:
            weights["authority"] *= 1.2
            weights["learning"] *= 0.7

        # -------------------------
        # LEARNING BOOST
        # -------------------------
        weights["learning"] += learning_boost

        # -------------------------
        # FEEDBACK CORRECTION
        # -------------------------
        confidence += (
            bias * weights["learning"]
            + feedback_bias * weights["feedback"]
        )

        # -------------------------
        # FINAL BIAS COMPUTATION
        # -------------------------
        authority_pressure = weights["authority"] * 0.4
        learning_pressure = weights["learning"] * 0.3
        regime_pressure = weights["regime"] * 0.2
        feedback_pressure = weights["feedback"] * 0.1

        decision_bias = (
            authority_pressure +
            learning_pressure +
            regime_pressure +
            feedback_pressure
        )

        return {
            "weights": weights,
            "confidence": round(confidence, 4),
            "decision_bias": round(decision_bias, 4),
            "regime": regime
        }

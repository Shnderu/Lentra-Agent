from typing import Dict, Any


class SignalPolicyKernel:

    def apply(self, meta: Dict[str, Any]) -> Dict[str, Any]:

        regime = meta.get("regime", {}).get("regime", "unknown")
        confidence = meta.get("confidence", 0.7)
        drift = meta.get("drift", {}).get("drift_score", 0.0)

        learning = meta.get("learning", {})
        feedback = meta.get("feedback", {})

        learning_tuning = learning.get("confidence_tuning", 0.0)
        feedback_bias = feedback.get("bias_correction", 0.0)

        # -------------------------
        # DEFAULT POLICY STATE
        # -------------------------
        policy = {
            "signal_amplification": 1.0,
            "risk_sensitivity": 1.0,
            "learning_weight": 1.0,
            "authority_weight": 1.0,
            "regime_bias": 0.0,
        }

        # -------------------------
        # REGIME-BASED POLICY SHIFT
        # -------------------------
        if regime == "bull":
            policy["signal_amplification"] = 1.2
            policy["learning_weight"] = 1.3
            policy["authority_weight"] = 0.9
            policy["regime_bias"] = 0.05

        elif regime == "bear":
            policy["signal_amplification"] = 0.9
            policy["learning_weight"] = 0.8
            policy["authority_weight"] = 1.3
            policy["regime_bias"] = -0.05

        elif regime == "volatile":
            policy["signal_amplification"] = 0.7
            policy["risk_sensitivity"] = 1.4
            policy["authority_weight"] = 1.5

        # -------------------------
        # DRIFT RESPONSE
        # -------------------------
        if drift > 0.1:
            policy["signal_amplification"] *= 0.8
            policy["authority_weight"] *= 1.2

        # -------------------------
        # LEARNING INJECTION
        # -------------------------
        policy["learning_weight"] += learning_tuning

        # -------------------------
        # FEEDBACK INJECTION
        # -------------------------
        confidence += feedback_bias * policy["learning_weight"]

        # -------------------------
        # FINAL POLICY SCORE
        # -------------------------
        policy_score = (
            policy["signal_amplification"] * 0.3 +
            policy["risk_sensitivity"] * 0.25 +
            policy["learning_weight"] * 0.25 +
            policy["authority_weight"] * 0.2
        )

        return {
            "policy": policy,
            "policy_score": round(policy_score, 4),
            "adjusted_confidence": round(confidence, 4)
        }

from typing import Dict, Any


class GovernanceLock:

    WEIGHTS = {
        "authority": 1.2,
        "policy": 1.0,
        "regime": 1.0,
        "learning": 1.0,
        "feedback": 1.0,
        "stability": 1.0,
    }

    @staticmethod
    def stabilize(meta: Dict[str, Any]) -> Dict[str, Any]:

        confidence = meta.get("confidence", 0.7)
        regime = meta.get("regime", {}).get("regime", "stable")

        # deterministic clamp
        confidence = max(0.5, min(0.85, confidence))

        # regime stabilization bias
        if regime == "bull":
            confidence += 0.02
        elif regime == "bear":
            confidence -= 0.02

        confidence = max(0.5, min(0.9, confidence))

        return {
            "weights": GovernanceLock.WEIGHTS,
            "confidence": round(confidence, 3),
            "regime": regime,
            "locked": True
        }

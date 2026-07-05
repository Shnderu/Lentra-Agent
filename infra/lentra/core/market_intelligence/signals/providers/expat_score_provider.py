from typing import Dict, Any


class ExpatScoreProvider:
    """
    Expat Fit Score (MVP layer)
    - не влияет на decision
    - используется для будущего ranking boost
    """

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        query = engine_outputs.get("query", "").lower()

        base = 0.75

        # lifestyle signals
        has_wifi = 0.9
        near_beach = 0.85 if "beach" in query else 0.75
        central = 0.8 if "center" in query else 0.7

        safety_proxy = 0.8

        expat_score = (
            base * 0.3 +
            has_wifi * 0.25 +
            near_beach * 0.25 +
            central * 0.1 +
            safety_proxy * 0.1
        )

        return {
            "score": round(expat_score, 4),
            "wifi": has_wifi,
            "beach_fit": near_beach,
            "central_fit": central,
            "safety_proxy": safety_proxy,
            "version": "expat_score_v1_safe"
        }

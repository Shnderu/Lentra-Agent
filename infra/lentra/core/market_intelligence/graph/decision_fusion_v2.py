from typing import Dict, Any


class DecisionFusionV2:
    """
    SAFE OS INTELLIGENCE GRAPH LAYER v2

    NON-BREAKING ENRICH LAYER:
    - consumes graph output
    - produces decision signal
    - does NOT modify engines
    """

    def __init__(self):
        self.version = "v2-safe-fusion"

    def enrich(self, graph_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert graph output → decision layer
        """

        pricing = graph_payload.get("pricing", {})
        risk = graph_payload.get("risk", {})
        dedup = graph_payload.get("dedup", {})
        expat = graph_payload.get("expat", {})

        score = pricing.get("score", 0.5)

        risk_level = risk.get("risk_level", 0.5)

        duplicates = dedup.get("matches", 1)

        # SAFE decision logic (non-aggressive, monotonic)
        if score > 0.85 and risk_level < 0.6:
            verdict = "strong_buy"
        elif score > 0.7:
            verdict = "buy"
        elif score < 0.4:
            verdict = "avoid"
        else:
            verdict = "neutral"

        confidence = (
            (1.0 - risk_level) * 0.5 +
            score * 0.4 +
            min(1.0, 1.0 / max(duplicates, 1)) * 0.1
        )

        return {
            "decision_v2": {
                "verdict": verdict,
                "confidence": round(confidence, 4),
                "signals": {
                    "pricing_score": score,
                    "risk_level": risk_level,
                    "dedup_pressure": duplicates,
                    "area_context": expat.get("area_score", 0.5),
                },
                "meta": {
                    "layer": self.version
                }
            }
        }

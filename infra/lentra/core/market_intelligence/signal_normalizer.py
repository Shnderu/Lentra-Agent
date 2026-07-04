from typing import Dict, Any


class SignalNormalizer:
    """
    Signal Normalization Layer v0.9 (LOCKED)

    PURPOSE:
    - stabilize ranking input signals
    - eliminate drift between restarts
    - enforce deterministic weighting
    """

    def __init__(self):
        # HARD LOCKED WEIGHTS (DO NOT TUNE WITHOUT VERSION BUMP)
        self.weights = {
            "pricing": 0.45,
            "area": 0.25,
            "risk": 0.20,
            "coupling": 0.10
        }

    def normalize(self, signals: Dict[str, Any]) -> Dict[str, Any]:

        pricing = signals.get("pricing", {})
        area = signals.get("area", {})
        risk = signals.get("risk", {})
        coupling = signals.get("coupling", {})

        # SAFE DEFAULTS (NO NULL PROPAGATION)
        pricing_score = float(pricing.get("score", 0.5))
        area_score = float(area.get("score", 0.5))
        risk_score = float(risk.get("risk_level", 0.5))
        coupling_score = float(coupling.get("score", 0.5))

        # HARD CLAMP
        pricing_score = max(0.0, min(1.0, pricing_score))
        area_score = max(0.0, min(1.0, area_score))
        risk_score = max(0.0, min(1.0, risk_score))
        coupling_score = max(0.0, min(1.0, coupling_score))

        # NORMALIZED COMPOSITE SIGNAL
        composite = (
            pricing_score * self.weights["pricing"] +
            area_score * self.weights["area"] +
            (1.0 - risk_score) * self.weights["risk"] +
            coupling_score * self.weights["coupling"]
        )

        return {
            "normalized": {
                "pricing": pricing_score,
                "area": area_score,
                "risk": risk_score,
                "coupling": coupling_score
            },
            "composite_score": round(composite, 6),
            "weights": self.weights,
            "version": "signal_norm_v0.9_locked"
        }

from typing import Dict, Any


class SignalNormalizerV09:
    """
    Signal Normalization Layer v0.9

    GOAL:
    - guarantee signal completeness
    - enforce 0..1 bounds
    - stabilize downstream ranking/risk coupling
    """

    def normalize(self, result: Dict[str, Any]) -> Dict[str, Any]:

        signals = result.get("signals") or {}

        # -----------------------
        # PRICING NORMALIZATION
        # -----------------------
        pricing = signals.get("pricing") or {}
        pricing_score = float(pricing.get("score") or 0.0)

        # clamp
        pricing_score = max(0.0, min(1.0, pricing_score))

        pricing["score"] = pricing_score
        pricing.setdefault("confidence", 0.9)

        # -----------------------
        # AREA NORMALIZATION
        # -----------------------
        area = signals.get("area") or {}
        area_score = float(area.get("score") or 0.0)
        area["score"] = max(0.0, min(1.0, area_score))

        if "country" not in area:
            area["country"] = "Vietnam"

        # -----------------------
        # COUPLING NORMALIZATION
        # -----------------------
        coupling = signals.get("coupling") or {}
        coupling_score = float(coupling.get("score") or 0.0)

        coupling["score"] = max(0.0, min(1.0, coupling_score))

        # -----------------------
        # REASSEMBLE
        # -----------------------
        signals["pricing"] = pricing
        signals["area"] = area
        signals["coupling"] = coupling

        result["signals"] = signals

        return result

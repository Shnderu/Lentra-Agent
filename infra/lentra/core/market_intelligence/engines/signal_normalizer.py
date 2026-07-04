from typing import Dict, Any


class SignalNormalizer:
    """
    Signal Normalization Layer v0.9

    PURPOSE:
    - unify raw engine signals into stable vector space
    - prevent ranking drift caused by signal variance
    """

    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})

        pricing = signals.get("pricing", {})
        area = signals.get("area", {})
        risk = data.get("risk", {})

        # -------------------------
        # HARD NORMALIZATION RULES
        # -------------------------

        price_score = float(pricing.get("score", 0.0))
        area_score = float(area.get("score", 0.0))
        risk_score = float(risk.get("risk_level", 0.0))

        # clamp safety
        price_score = max(0.0, min(1.0, price_score))
        area_score = max(0.0, min(1.0, area_score))
        risk_score = max(0.0, min(1.0, risk_score))

        # coupling stabilization
        coupling_raw = signals.get("coupling", {}).get("score", 0.0)
        coupling_score = max(0.0, min(1.0, coupling_raw))

        # -------------------------
        # SIGNAL VECTOR (CORE FIX)
        # -------------------------

        signal_vector = {
            "price": price_score,
            "area": area_score,
            "risk": 1.0 - risk_score,   # invert (safe = high)
            "coupling": coupling_score
        }

        # -------------------------
        # WRITE BACK STABLE FORMAT
        # -------------------------

        data["signal_vector"] = signal_vector

        # normalize signals block too
        data["signals"]["pricing"]["score"] = price_score
        data["signals"]["area"]["score"] = area_score

        if "coupling" in data["signals"]:
            data["signals"]["coupling"]["score"] = coupling_score

        return data

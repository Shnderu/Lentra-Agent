from typing import Dict, Any


class SignalNormalizationLayerV2:
    """
    Signal Normalization Layer v2

    PURPOSE:
    - unify heterogeneous signals into stable bounded space
    - prepare inputs for ranking + decision layer
    """

    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})

        # ------------------------
        # pricing normalization
        # ------------------------
        pricing = signals.get("pricing", {})
        pricing_score = float(pricing.get("score", 0.0))
        pricing_score = max(0.0, min(1.0, pricing_score))

        pricing_conf = float(pricing.get("confidence", pricing_score))
        pricing_conf = max(0.0, min(1.0, pricing_conf))

        # ------------------------
        # area normalization
        # ------------------------
        area = signals.get("area", {})
        area_score = float(area.get("score", 0.5))
        area_score = 0.5 + (area_score * 0.5)  # compress into [0.5..1.0]

        # ------------------------
        # coupling normalization
        # ------------------------
        coupling = signals.get("coupling", {})
        coupling_score = float(coupling.get("score", 0.0))
        coupling_score = max(0.0, min(1.0, coupling_score))

        entropy = float(coupling.get("factors", {}).get("entropy", 0.0))
        entropy_dampener = 1 - min(1.0, entropy)

        coupling_score = coupling_score * entropy_dampener

        # ------------------------
        # risk normalization
        # ------------------------
        risk = data.get("risk", {})
        risk_level = float(risk.get("risk_level", 0.0))
        risk_level = max(0.0, min(1.0, risk_level))

        # ------------------------
        # write back normalized signals
        # ------------------------
        signals["pricing"]["score"] = pricing_score
        signals["pricing"]["confidence"] = pricing_conf

        signals["area"]["score"] = area_score

        signals["coupling"]["score"] = coupling_score

        data["risk"]["risk_level"] = risk_level

        data["signals"] = signals
        data["signals"]["_normalized"] = True

        return data

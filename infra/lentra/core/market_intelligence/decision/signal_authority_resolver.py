from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class SignalAuthorityResult:
    final_risk_level: str
    final_verdict: str
    adjusted_confidence: float
    authority_trace: Dict[str, Any]


class SignalAuthorityResolver:

    """
    v1 authority resolver:
    - resolves conflicts between pricing / risk / dedup / expat
    - enforces signal hierarchy
    """

    # HARD AUTHORITY (can override everything)
    HARD = {
        "risk_level",
        "fraud_score",
    }

    # STRUCTURAL (high weight, but not override)
    STRUCTURAL = {
        "market_price",
        "duplicates",
    }

    # CONTEXTUAL (influence only)
    CONTEXTUAL = {
        "area_score",
        "internet_score",
        "noise_score",
        "safety_score",
    }

    # DERIVED
    DERIVED = {
        "deviation_pct",
        "confidence",
        "verdict",
    }

    def resolve(self, ui: Dict[str, Any], api: Dict[str, Any], meta: Dict[str, Any]) -> SignalAuthorityResult:

        trace = {
            "applied_rules": [],
            "conflicts": [],
        }

        risk = ui.get("risk_level", "unknown")
        deviation = ui.get("deviation_pct", 0)
        duplicates = ui.get("duplicates", 0)
        verdict = ui.get("verdict", "ok")

        confidence = meta.get("confidence", 0.72)

        # -------------------------
        # RULE 1: RISK OVERRIDE
        # -------------------------
        if risk == "high":
            trace["applied_rules"].append("risk_override_high")
            verdict = "risk_high"
            confidence -= 0.2

        # -------------------------
        # RULE 2: DUPLICATE DOMINANCE
        # -------------------------
        if duplicates >= 5:
            trace["applied_rules"].append("duplicate_override")
            verdict = "likely_duplicate"
            confidence -= 0.1

        # -------------------------
        # RULE 3: PRICE DEVIATION BIAS
        # -------------------------
        if deviation > 25:
            trace["applied_rules"].append("overprice_strong_signal")
            if risk != "high":
                verdict = "overpriced"
            confidence -= 0.1

        if deviation < -20:
            trace["applied_rules"].append("underprice_signal")
            verdict = "underpriced"
            confidence -= 0.05

        # -------------------------
        # RULE 4: CONTEXT BOOST / PENALTY
        # -------------------------
        area_score = api.get("signals", {}).get("area_score", 0)

        if area_score < 0.4:
            trace["applied_rules"].append("low_area_penalty")
            confidence -= 0.05

        if area_score > 0.8:
            trace["applied_rules"].append("high_area_boost")
            confidence += 0.03

        # -------------------------
        # NORMALIZATION
        # -------------------------
        confidence = max(0.1, min(0.95, confidence))

        return SignalAuthorityResult(
            final_risk_level=risk,
            final_verdict=verdict,
            adjusted_confidence=confidence,
            authority_trace=trace
        )

from typing import Dict, Any


class IntelligenceNormalizer:
    """
    Normalize Market Intelligence engine outputs.

    Goal:
    keep one stable product contract:

    intelligence:
        area
        market
        risk
        dedup
    """

    def normalize_risk(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return {}

        risk = data.get("risk", {})

        if isinstance(risk, dict) and "risk" in risk:
            risk = risk["risk"]

        return risk


    def normalize_dedup(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return {}

        dedup = data.get("dedup", {})

        if isinstance(dedup, dict) and "dedup" in dedup:
            dedup = dedup["dedup"]

        return dedup


    def build_intelligence(
        self,
        area: Dict[str, Any],
        market: Dict[str, Any],
        risk: Dict[str, Any],
        dedup: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {
            "area": area or {},
            "market": market or {},
            "risk": self.normalize_risk(risk),
            "dedup": self.normalize_dedup(dedup),
        }

from typing import Dict, Any


class EngineOutputNormalizer:
    """
    Normalize engine outputs into clean product contracts.

    Goal:
    - engines return only their intelligence block
    - remove recursive nested payloads
    - keep API output stable
    """

    @staticmethod
    def normalize_risk(data: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return {}

        risk = data.get("risk", {})

        if not isinstance(risk, dict):
            risk = {}

        return {
            "fraud_score": risk.get(
                "fraud_score",
                0.0
            ),
            "level": risk.get(
                "level",
                "unknown"
            ),
            "price_signal": risk.get(
                "price_signal",
                "unknown"
            ),
            "deviation": risk.get(
                "deviation",
                0.0
            ),
            "source": risk.get(
                "source",
                "unknown"
            ),
            "status": risk.get(
                "status",
                "ok"
            )
        }


    @staticmethod
    def normalize_dedup(data: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return {}

        dedup = data.get(
            "dedup",
            {}
        )

        if not isinstance(dedup, dict):
            return {}

        return {
            "duplicates": dedup.get(
                "duplicates",
                0
            ),
            "confidence": dedup.get(
                "confidence",
                0.0
            ),
            "sources": dedup.get(
                "sources",
                []
            ),
            "canonical_listing": dedup.get(
                "canonical_listing"
            ),
            "fingerprint": dedup.get(
                "fingerprint"
            ),
            "status": dedup.get(
                "status",
                "unknown"
            )
        }


    @staticmethod
    def normalize_all(
        risk: Dict[str, Any],
        dedup: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {
            "risk": EngineOutputNormalizer.normalize_risk(
                risk
            ),
            "dedup": EngineOutputNormalizer.normalize_dedup(
                dedup
            )
        }

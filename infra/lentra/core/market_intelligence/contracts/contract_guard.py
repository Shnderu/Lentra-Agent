from typing import Dict, Any


class ContractGuard:
    """
    Ensures Market Intelligence output integrity.
    No transformation logic — only validation + safety fallback.
    """

    REQUIRED_KEYS = {"ui", "api", "meta"}

    def validate(self, result: Dict[str, Any]) -> bool:
        if not isinstance(result, dict):
            return False

        return self.REQUIRED_KEYS.issubset(set(result.keys()))

    def safe_wrap(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Guarantees stable contract even on engine failure.
        """

        if not isinstance(result, dict):
            result = {}

        return {
            "ui": result.get("ui", {
                "price": None,
                "market_price": None,
                "deviation_pct": 0.0,
                "risk_level": "unknown",
                "duplicates": 0,
                "verdict": "unknown",
            }),
            "api": result.get("api", {
                "vector": {},
                "spine": {
                    "verdict": "unknown",
                    "confidence": 0.0,
                    "risk_level": "unknown",
                },
            }),
            "meta": result.get("meta", {
                "trace_id": "guard-fallback",
                "confidence": 0.0,
                "regime": {"regime": "unknown"},
                "governance": {
                    "weights": {},
                    "confidence": 0.0,
                    "regime": "unknown",
                    "locked": False,
                },
            }),
        }

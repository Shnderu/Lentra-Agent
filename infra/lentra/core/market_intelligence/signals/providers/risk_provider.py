from typing import Dict, Any


class RiskSignalProvider:
    name = "risk"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        raw = engine_outputs.get("risk", {})

        level = raw.get("risk_level", 0.0)

        return {
            "score": float(level),
            "confidence": 1.0,
            "meta": {
                "level": level
            },
        }

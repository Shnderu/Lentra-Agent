from typing import Dict, Any


class AreaSignalProvider:
    name = "area"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        raw = engine_outputs.get("area", {})

        return {
            "score": float(raw.get("score", 0.0)),
            "confidence": 1.0,
            "meta": raw,
        }

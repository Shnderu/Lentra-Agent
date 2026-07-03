from typing import Dict, Any


class PricingSignalProvider:
    name = "pricing"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        raw = engine_outputs.get("pricing", {})

        score = float(raw.get("score", 0.0))

        direction = raw.get("direction", "neutral")
        deviation = float(raw.get("deviation", 0.0))

        return {
            "score": score,
            "confidence": 1.0,
            "meta": {
                "direction": direction,
                "deviation": deviation,
            },
        }

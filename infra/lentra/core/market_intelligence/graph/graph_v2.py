from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GraphV2:
    """
    SAFE GRAPH LAYER v2
    ONLY projection layer - no intelligence logic
    """

    enabled: bool = True

    def build(self, payload: Dict[str, Any], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "facts": engine_outputs,
            "features": self._extract_features(engine_outputs),
            "derived": self._derive_signals(payload, engine_outputs),
            "signals": self._aggregate_signals(engine_outputs),
        }

    def _extract_features(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price_bucket": "high" if engine_outputs.get("pricing", {}).get("score", 0) > 0.8 else "mid"
        }

    def _derive_signals(self, payload: Dict[str, Any], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "normalized_delta": engine_outputs.get("pricing", {}).get("delta", 0)
        }

    def _aggregate_signals(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:

        risk = engine_outputs.get("risk", {})
        decision = engine_outputs.get("decision", {})
        pricing = engine_outputs.get("pricing", {})
        area = engine_outputs.get("area", {})

        return {
            "risk_level": risk.get("risk_level", 0),

            "price_deviation": pricing.get("delta", 0),
            "price_score": pricing.get("score", 0),

            "fraud_probability": risk.get("fraud_probability", 0),

            "area_score": area.get("score", 0),

            "decision": decision.get("verdict", "neutral"),
        }

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GraphV2:
    """
    SAFE GRAPH LAYER v2
    IMPORTANT:
    - NOT intelligence engine
    - NOT decision layer
    - ONLY projection of existing outputs
    """

    enabled: bool = True

    def build(self, payload: Dict[str, Any], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        SAFE PURE TRANSFORM LAYER
        """
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
        return {
            "risk": engine_outputs.get("risk", {}).get("risk_level", 0),
            "signal": engine_outputs.get("decision", {}).get("verdict", "neutral")
        }

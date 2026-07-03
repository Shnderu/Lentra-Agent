from dataclasses import dataclass
from typing import Dict, Any

from lentra.core.market_intelligence.signals.signal_registry import SignalRegistry


@dataclass
class GraphV2:
    """
    SAFE GRAPH LAYER v2

    - ONLY projection layer
    - signals come from registry (single authority)
    """

    enabled: bool = True

    def __post_init__(self):
        self.registry = SignalRegistry()

    def build(self, payload: Dict[str, Any], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:

        signals = self.registry.build(engine_outputs)

        return {
            "facts": engine_outputs,
            "features": self._extract_features(engine_outputs),
            "derived": self._derive_signals(payload, engine_outputs),
            "signals": signals,
        }

    def _extract_features(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price_bucket": "high" if engine_outputs.get("pricing", {}).get("score", 0) > 0.8 else "mid"
        }

    def _derive_signals(self, payload: Dict[str, Any], engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "normalized_delta": engine_outputs.get("pricing", {}).get("deviation", 0)
        }

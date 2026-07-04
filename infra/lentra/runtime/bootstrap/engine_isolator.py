from typing import Dict, Any
from lentra.core.market_intelligence.normalization.signal_normalizer import SignalNormalizer


class EngineIsolator:
    """
    Contract Stabilization Layer v1.2

    PIPELINE ORDER (LOCKED):
    1. compute()
    2. normalize signals (v0.9)
    3. return stable contract
    """

    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines or {}
        self.normalizer = SignalNormalizer()

    def run_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        engine = self.engines.get("market_intelligence")

        if engine is None:
            return {
                "score": 0.0,
                "decision": "NO_ENGINE",
                "error": "market_intelligence engine not registered"
            }

        # -------------------------
        # SINGLE SOURCE OF TRUTH
        # -------------------------
        if hasattr(engine, "compute"):
            result = engine.compute(payload)
        else:
            result = engine.fetch(payload)

        # -------------------------
        # SIGNAL NORMALIZATION LAYER v0.9
        # -------------------------
        result = self.normalizer.normalize(result)

        # -------------------------
        # CONTRACT STABILIZATION
        # -------------------------
        if isinstance(result, dict):
            result.setdefault("dedup", {})
            result.setdefault("ranking", {})
            result.setdefault("risk", {})
            result.setdefault("signals", {})
            result.setdefault("features", {})

        return result

from typing import Dict, Any


class EngineIsolator:
    """
    Isolator V2 FIXED CONTRACT LAYER

    Strategy:
    - single-call execution model
    - engine.compute(payload) is canonical contract
    - no pipeline assumptions (fetch/normalize/dedup/rank/risk)
    - backward-compatible output passthrough
    """

    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines or {}

    def run_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        engine = self.engines.get("market_intelligence")

        if engine is None:
            return {
                "score": 0.0,
                "decision": "NO_ENGINE",
                "error": "market_intelligence engine not registered"
            }

        # =========================
        # V2 FIXED EXECUTION MODEL
        # =========================
        if hasattr(engine, "compute"):
            data = engine.compute(payload)
        else:
            # fallback safety (legacy compatibility)
            data = self._legacy_fallback(engine, payload)

        return data

    def _legacy_fallback(self, engine: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Minimal compatibility layer for old engines (if any remain).
        """
        data = engine.fetch(payload)
        data = engine.normalize(data)
        data = engine.dedup(data)
        data = engine.rank(data)
        data = engine.risk(data)

        if hasattr(engine, "build"):
            data = engine.build(data)

        return data

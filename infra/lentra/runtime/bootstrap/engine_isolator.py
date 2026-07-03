from typing import Dict, Any


class EngineIsolator:
    """
    Canonical isolation layer for Market Intelligence engines.
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

        data = engine.fetch(payload)
        data = engine.normalize(data)
        data = engine.dedup(data)
        data = engine.rank(data)
        data = engine.risk(data)

        # NEW SIGNALS LAYER
        if hasattr(engine, "build"):
            data = engine.build(data)

        return data

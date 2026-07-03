from typing import Dict, Any


class EngineIsolator:
    """
    Canonical isolation layer for Market Intelligence engines.
    Responsible ONLY for orchestration, NOT logic.
    """

    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines or {}

    def run_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        SAFE execution pipeline:
        fetch → normalize → dedup → rank → risk → graph
        """

        engine = self.engines.get("market_intelligence")
        if engine is None:
            return {
                "score": 0.0,
                "decision": "NO_ENGINE",
                "error": "market_intelligence engine not registered"
            }

        result = engine.fetch(payload)

        result = engine.normalize(result)
        result = engine.dedup(result)
        result = engine.rank(result)
        result = engine.risk(result)

        # graph projection (optional safe layer)
        if hasattr(engine, "graph"):
            result = engine.graph.build(payload, result)

        return result

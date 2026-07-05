from typing import Dict, Any


class ExpatProvider:
    """
    Converts expat engine output into normalized signal
    for signals_engine_v1 compatibility
    """

    def __init__(self, expat_engine):
        self.engine = expat_engine

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        raw = self.engine.compute(engine_outputs)

        score = raw.get("score", 0.5)

        return {
            "score": score,
            "tier": raw.get("tier", "MEDIUM"),
            "features": raw.get("features", {}),
            "normalized": min(1.0, max(0.0, score))
        }

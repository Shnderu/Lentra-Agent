from typing import Dict, Any


class EngineIsolator:
    """
    COMPAT LAYER
    Bridges legacy gateway_v3 expectations -> real isolation engine
    """

    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines

        # lazy import real engine
        from lentra.core.market_intelligence.isolation.engine_isolator import EngineIsolator as RealEngine
        self.real = RealEngine()

    def run_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        SAFE ENTRYPOINT
        """

        try:
            if hasattr(self.real, "run_all"):
                return self.real.run_all(payload)

            if hasattr(self.real, "run"):
                return self.real.run(payload)

            # fallback safe output
            return {
                "score": 0.0,
                "decision": "NO_RUN_METHOD",
                "features": {},
                "weights": {}
            }

        except Exception as e:
            return {
                "score": 0.0,
                "decision": "ISOLATOR_CRASH",
                "error": str(e)
            }

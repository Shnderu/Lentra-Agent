from typing import Dict, Any
from lentra.core.market_intelligence.isolation.engine_isolator import EngineIsolator


class EngineRegistryV3:
    """
    CLEAN REGISTRY:
    - only real engines
    - no dict engines
    - no raw access
    """

    def __init__(self, engines: Dict[str, Any]):
        self._engines = {
            name: EngineIsolator(engine)
            for name, engine in engines.items()
        }

    def list(self):
        return {
            "active": list(self._engines.keys()),
            "total": len(self._engines)
        }

    def run_all(self, payload: Dict[str, Any], ctx: Dict[str, Any]):
        result = {}

        for name, engine in self._engines.items():
            result[name] = engine.evaluate(payload, result, ctx)

        return result

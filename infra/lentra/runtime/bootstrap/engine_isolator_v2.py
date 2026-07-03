from typing import Dict, Any


class EngineIsolatorV2:
    """
    Contract-aware execution layer (safe rollout version)

    Key goals:
    - backward compatible with existing engine API
    - graceful fallback if stages are missing
    - no hard dependency on engine method set
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

        data = self._safe_call(engine, "fetch", payload)
        data = self._safe_call(engine, "normalize", data)

        # core pipeline (safe staged execution)
        data = self._safe_call(engine, "dedup", data)
        data = self._safe_call(engine, "rank", data)
        data = self._safe_call(engine, "risk", data)

        # optional enrichment
        if hasattr(engine, "build"):
            try:
                data = engine.build(data)
            except Exception as e:
                data = {
                    **data,
                    "build_error": str(e)
                }

        return data

    def _safe_call(self, engine, method: str, data: Any) -> Any:
        fn = getattr(engine, method, None)

        if callable(fn):
            try:
                return fn(data)
            except Exception as e:
                return {
                    **(data if isinstance(data, dict) else {}),
                    f"{method}_error": str(e),
                    f"{method}_fallback": True
                }

        return data

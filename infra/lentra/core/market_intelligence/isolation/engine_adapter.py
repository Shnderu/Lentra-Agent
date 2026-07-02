from typing import Any, Dict


class EngineResult(dict):
    """
    Unified contract object for all engines.
    """

    def ok(self) -> bool:
        return self.get("status") == "ok"


class EngineAdapter:
    """
    V3 contract enforcement layer:
    - ensures consistent output schema
    - wraps legacy dict engines
    - prevents nested drift
    """

    def __init__(self, engine: Any, name: str):
        self.engine = engine
        self.name = name

    def evaluate(self, payload: Dict[str, Any]) -> EngineResult:
        try:
            raw = self.engine.evaluate(payload)

            # normalize None / dict / object
            if raw is None:
                return EngineResult({
                    "status": "failed",
                    "engine": self.name,
                    "error": "EMPTY_RESULT"
                })

            if isinstance(raw, EngineResult):
                raw["engine"] = self.name
                return raw

            if isinstance(raw, dict):
                return EngineResult({
                    "status": raw.get("status", "ok"),
                    "engine": self.name,
                    **raw
                })

            # fallback
            return EngineResult({
                "status": "ok",
                "engine": self.name,
                "data": raw
            })

        except Exception as e:
            return EngineResult({
                "status": "failed",
                "engine": self.name,
                "error": str(e)
            })

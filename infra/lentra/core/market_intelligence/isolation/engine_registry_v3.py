from __future__ import annotations

from typing import Any, Dict
import inspect


class EngineRegistryV3:
    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines or {}
        self.active = list(self.engines.keys())

    def list_engines(self) -> Dict[str, Any]:
        return {
            "active": self.active,
            "total": len(self.engines),
        }

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        for name, engine in self.engines.items():
            result[name] = self._safe_call(name, engine, payload)

        return self._normalize(result)

    def _safe_call(self, name: str, engine: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            fn = getattr(engine, "evaluate", None)

            if fn is None:
                return {"status": "failed", "error": f"{name}.evaluate not found"}

            sig = inspect.signature(fn)
            params = list(sig.parameters.keys())

            # FIX: unified contract (NO ctx wrapper assumption)
            if len(params) == 2:
                # (self, payload)
                return fn(payload)

            if len(params) >= 3:
                # (self, payload, result)
                return fn(payload, {})

            return fn(payload)

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
            }

    def _normalize(self, result: Dict[str, Any]) -> Dict[str, Any]:
        normalized: Dict[str, Any] = {}

        for k, v in result.items():
            if v is None:
                normalized[k] = {"status": "failed", "error": "null_result"}
                continue

            if not isinstance(v, dict):
                normalized[k] = {"status": "ok", "value": v}
                continue

            normalized[k] = v

        return normalized


def build_registry_v3(engines: Dict[str, Any]) -> EngineRegistryV3:
    return EngineRegistryV3(engines)

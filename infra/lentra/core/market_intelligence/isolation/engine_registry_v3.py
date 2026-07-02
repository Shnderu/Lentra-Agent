from __future__ import annotations

from typing import Any, Dict


class EngineRegistryV3:
    """
    FIXED Production Engine Isolation Layer V3

    CHANGE:
    - removed broken inspect-based ABI detection
    - replaced with deterministic dual-call strategy
    """

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

            # ----------------------------
            # FIX: NO introspection (broken in bound methods)
            # ----------------------------

            # try V3 style first (context, result)
            try:
                return fn(payload, {})
            except TypeError:
                pass

            # fallback V2 style (payload only OR ctx-like object)
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

            if k in v and isinstance(v[k], dict):
                normalized[k] = v[k]
                continue

            normalized[k] = v

        return normalized


def build_registry_v3(engines: Dict[str, Any]) -> EngineRegistryV3:
    return EngineRegistryV3(engines)

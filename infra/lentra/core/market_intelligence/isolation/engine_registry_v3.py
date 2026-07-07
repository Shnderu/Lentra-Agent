from __future__ import annotations

from typing import Any, Dict


class EngineRegistryV3:
    """
    Sequential market intelligence engine pipeline.

    Contract:

    input:
        raw payload

    flow:
        engine_1
        engine_2
        engine_3
        ...

    output:
        accumulated intelligence context
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

        context = dict(payload)

        for name, engine in self.engines.items():

            result = self._safe_call(
                name,
                engine,
                context
            )

            if isinstance(result, dict):
                context.update(result)

        return context

    def _safe_call(
        self,
        name: str,
        engine: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            fn = getattr(engine, "evaluate", None)

            if fn is None:
                return {
                    name: {
                        "status": "failed",
                        "error": "evaluate_missing"
                    }
                }

            result = fn(context)

            if isinstance(result, dict):
                return result

            return {
                name: {
                    "status": "ok",
                    "value": result
                }
            }

        except Exception as e:

            return {
                name: {
                    "status": "failed",
                    "error": str(e)
                }
            }


def build_registry_v3(
    engines: Dict[str, Any]
) -> EngineRegistryV3:

    return EngineRegistryV3(engines)

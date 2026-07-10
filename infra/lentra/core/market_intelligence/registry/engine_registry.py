from typing import Dict, Any


class EngineRegistry:
    """
    MARKET INTELLIGENCE ENGINE REGISTRY

    Single runtime registry.

    Responsibilities:
    - hold active intelligence engines
    - execute engines sequentially
    - accumulate intelligence context

    Does NOT:
    - discover engines dynamically
    - own business logic
    - contain graph/workflow execution
    """

    def __init__(self, engines: Dict[str, Any]):
        self._engines = engines or {}

    def list(self):
        return {
            "active": list(self._engines.keys()),
            "total": len(self._engines)
        }

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        context = dict(payload)

        for name, engine in self._engines.items():

            try:
                fn = getattr(engine, "evaluate", None)

                if fn is None:
                    context[name] = {
                        "status": "failed",
                        "error": "evaluate_missing"
                    }
                    continue

                result = fn(context)

                if isinstance(result, dict):
                    context.update(result)
                else:
                    context[name] = {
                        "status": "ok",
                        "value": result
                    }

            except Exception as exc:

                context[name] = {
                    "status": "failed",
                    "error": str(exc)
                }

        return context


def build_registry(
    engines: Dict[str, Any]
) -> EngineRegistry:

    return EngineRegistry(engines)

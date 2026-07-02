from typing import Any, Dict


class SafeEngineWrapper:
    def __init__(self, engine: Any):
        self.engine = engine

    def evaluate(self, ctx: Any, result: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # new contract
            return self.engine.evaluate(ctx, result)
        except TypeError:
            # legacy fallback
            return self.engine.evaluate(ctx)
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

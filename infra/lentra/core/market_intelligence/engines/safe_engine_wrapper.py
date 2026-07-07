from typing import Any, Dict


class SafeEngineWrapper:
    """
    Unified engine adapter.

    Contract:
    input:
        accumulated result dict

    output:
        enriched result dict
    """

    def __init__(self, engine: Any):
        self.engine = engine

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(payload, dict):
            payload = {}

        try:
            fn = getattr(self.engine, "evaluate", None)

            if fn is None:
                return {
                    "status": "failed",
                    "error": "no_evaluate_method"
                }

            result = dict(payload)

            try:
                output = fn(result)
            except TypeError:
                output = fn(result, result)

            if output is None:
                return result

            if not isinstance(output, dict):
                return {
                    **result,
                    "engine_value": output
                }

            return output

        except Exception as e:
            return {
                **payload,
                "status": "failed",
                "error": str(e)
            }

from .base import EngineV3

class AreaEngine(EngineV3):
    name = "area"

    def evaluate(self, context: dict, result: dict):
        query = context.get("query", "")

        result["area"] = {
            "detected": "unknown",
            "query_hint": query
        }

        return result

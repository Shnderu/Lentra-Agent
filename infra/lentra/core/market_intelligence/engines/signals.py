from .base import EngineV3

class SignalsEngine(EngineV3):
    name = "signals"

    def evaluate(self, context: dict, result: dict):
        query = context.get("query", "")

        result["signals"] = {
            "length": len(query),
            "type": "rental_query" if "studio" in query else "generic"
        }

        return result

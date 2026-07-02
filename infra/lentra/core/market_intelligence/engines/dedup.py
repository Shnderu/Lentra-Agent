from .base import EngineV3

class DedupEngine(EngineV3):
    name = "dedup"

    def evaluate(self, context: dict, result: dict):
        result["dedup"] = {
            "duplicates": 0,
            "status": "no_index"
        }

        return result

from typing import Dict, Any


class AreaEngine:
    """
    V3 SAFE AREA ENGINE

    input:
        accumulated result dict

    output:
        enriched result dict
    """

    def evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        query = result.get("query", "")

        result["area"] = {
            "detected": "unknown",
            "query_hint": query[:20],
            "status": "ok"
        }

        return result

class AreaEngine:
    """
    V2 SAFE AREA ENGINE
    """

    def evaluate(self, payload, result):
        query = payload.get("query", "")

        result["area"] = {
            "detected": "unknown",
            "query_hint": query[:20]
        }

        return result

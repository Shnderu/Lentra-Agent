class SignalsEngine:
    """
    V2 SAFE SIGNAL ENGINE
    """

    def evaluate(self, payload, result):
        query = payload.get("query", "")

        result["signals"] = {
            "length": len(query),
            "type": "rental_query"
        }

        return result

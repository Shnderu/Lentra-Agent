from typing import Dict, Any


class QueryParser:
    """
    Core query parser for market intelligence search.

    Converts raw user query into structured intent.
    """

    def parse(self, query: str) -> Dict[str, Any]:
        query_l = query.lower()

        intent_type = "rent" if any(
            x in query_l for x in ["rent", "studio", "apartment", "flat"]
        ) else "unknown"

        location = None
        if "da nang" in query_l:
            location = "da nang"

        budget_max = None
        for token in query_l.split():
            if token.isdigit():
                budget_max = int(token)

        return {
            "query": query,
            "type": intent_type,
            "location": location,
            "budget_max": budget_max
        }

from typing import Dict, Any


class IntentNormalizer:
    """
    Minimal deterministic intent extraction layer.
    No ML, no external dependencies.
    """

    RENT_KEYWORDS = [
        "rent", "studio", "apartment", "flat",
        "beach", "cheap", "house"
    ]

    def normalize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        query = (request.get("query") or "").lower()

        intent_type = "rent" if any(k in query for k in self.RENT_KEYWORDS) else "general"

        location = self._extract_location(query)
        budget = self._extract_budget(query)

        return {
            "type": intent_type,
            "raw_query": request.get("query"),
            "location": location,
            "budget_max": budget
        }

    def _extract_location(self, query: str):
        for city in ["da nang", "bangkok", "bali", "chiang mai"]:
            if city in query:
                return city
        return None

    def _extract_budget(self, query: str):
        # ultra-simple heuristic
        if "cheap" in query:
            return 500
        return None


normalizer = IntentNormalizer()

from typing import Dict, Any


class IntentNormalizer:
    def build(self, query: str) -> Dict[str, Any]:
        q = (query or "").lower()

        intent = {
            "query": query
        }

        if any(x in q for x in ["studio", "apartment", "flat", "rent"]):
            intent["type"] = "rent"
        else:
            intent["type"] = "general"

        if "da nang" in q:
            intent["location"] = "da nang"

        if "cheap" in q:
            intent["budget_max"] = 500

        return intent


intent_normalizer = IntentNormalizer()

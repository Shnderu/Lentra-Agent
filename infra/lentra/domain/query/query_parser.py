import re
from typing import Dict, Any


class QueryParser:
    """
    Преобразует текстовый запрос в структурированные сигналы поиска.
    """

    def parse(self, text: str) -> Dict[str, Any]:
        text_l = text.lower()

        result = {
            "raw": text,
            "features": {},
            "boosts": {}
        }

        # budget intent
        if re.search(r"\bcheap\b|\blow cost\b|\bbudget\b", text_l):
            result["boosts"]["cheap"] = 0.3
            result["budget_tier"] = "low"

        if re.search(r"\bluxury\b|\bexpensive\b|\bpremium\b", text_l):
            result["boosts"]["luxury"] = 0.3
            result["budget_tier"] = "high"

        # features
        if "pool" in text_l:
            result["features"]["pool"] = True

        if "sea view" in text_l or "seaview" in text_l:
            result["features"]["sea_view"] = True

        if "pet" in text_l:
            result["features"]["pet_friendly"] = True

        # intent
        if "apartment" in text_l:
            result["intent"] = "rent_search"

        return result


def parse_query(text: str) -> Dict[str, Any]:
    """
    API ожидает именно эту функцию.
    """
    return QueryParser().parse(text)

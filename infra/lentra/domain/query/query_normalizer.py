import re
from typing import Dict, Any, List


class QueryNormalizer:
    """
    Приводит текстовый запрос к набору стандартных тегов (канонизация сигнала).
    Это промежуточный слой между parser и builder/ranking.
    """

    def normalize(self, text: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
        text_l = (text or "").lower()

        tags: List[str] = []

        # базовые intent-теги
        if parsed.get("intent"):
            tags.append(parsed["intent"])

        # price intent
        if "cheap" in text_l or "budget" in text_l:
            tags.append("budget_low")

        if "luxury" in text_l or "expensive" in text_l:
            tags.append("budget_high")

        # location intent (очень грубо пока)
        if "da nang" in text_l:
            tags.append("city_da_nang")

        # features normalization
        if "pool" in text_l:
            tags.append("feature_pool")

        if "sea" in text_l or "beach" in text_l or "sea view" in text_l:
            tags.append("feature_sea_view")

        if "pet" in text_l:
            tags.append("feature_pet")

        # lifestyle tags
        if "family" in text_l:
            tags.append("lifestyle_family")

        if "studio" in text_l:
            tags.append("type_studio")

        # cleanup duplicates
        tags = list(set(tags))

        return {
            "tags": tags,
            "raw": text,
            "parsed": parsed
        }

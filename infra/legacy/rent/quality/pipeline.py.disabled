from typing import List, Dict, Any


class RentQualityPipeline:
    """
    v1 quality layer:
    - normalization
    - scoring
    - sorting
    """

    def process(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = [self._normalize(i) for i in items]

        scored = [self._score(i) for i in normalized]

        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored

    def _normalize(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": item.get("title") or item.get("name") or "unknown",
            "price": item.get("price"),
            "location": item.get("location"),
            "raw": item
        }

    def _score(self, item: Dict[str, Any]) -> Dict[str, Any]:
        score = 0

        if item.get("price"):
            score += 10

        if item.get("location"):
            score += 5

        if item.get("title") != "unknown":
            score += 3

        item["score"] = score
        return item

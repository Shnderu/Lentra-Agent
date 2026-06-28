from typing import Any, Dict, List, Optional


class CanonicalSearchPipeline:
    """
    v3 SINGLE SOURCE OF TRUTH pipeline.

    Порядок:
    1. normalize
    2. deduplicate
    3. market enrichment (future)
    4. ranking (future)
    5. DTO output
    """

    def __init__(self, dedup_engine=None, market_engine=None, ranking_engine=None):
        self.dedup_engine = dedup_engine
        self.market_engine = market_engine
        self.ranking_engine = ranking_engine

    def run(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        objects = self._normalize(objects)
        objects = self._deduplicate(objects)
        objects = self._market(objects)
        objects = self._rank(objects)

        return objects

    def _normalize(self, objects):
        result = []

        for obj in objects:
            normalized = {
                "id": obj.get("id"),
                "title": obj.get("title") or obj.get("name"),
                "price": self._float(obj.get("price")),
                "currency": obj.get("currency", "USD"),
                "location": obj.get("location"),
                "source": obj.get("source"),
                "raw": obj,
            }

            if not normalized["title"]:
                continue

            result.append(normalized)

        return result

    def _deduplicate(self, objects):
        if self.dedup_engine:
            return self.dedup_engine.merge(objects)
        return objects

    def _market(self, objects):
        if self.market_engine:
            return self.market_engine.enrich(objects)
        return objects

    def _rank(self, objects):
        if self.ranking_engine:
            return self.ranking_engine.rank(objects)
        return objects

    def _float(self, v) -> Optional[float]:
        try:
            if v is None:
                return None
            return float(str(v).replace(",", "."))
        except Exception:
            return None

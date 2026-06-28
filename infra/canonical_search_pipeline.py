from typing import Any, Dict, List, Optional


class CanonicalSearchPipeline:
    """
    ЕДИНАЯ точка обработки search results.

    Назначение:
    - убрать разрозненную логику из API и сервисов
    - зафиксировать canonical object model
    - подготовить систему под Market Intelligence layer
    """

    def __init__(self, normalizer=None, dedup_engine=None):
        self.normalizer = normalizer
        self.dedup_engine = dedup_engine

    def run(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not objects:
            return []

        normalized = self._normalize(objects)
        deduped = self._deduplicate(normalized)

        return deduped

    def _normalize(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []

        for obj in objects:
            normalized = {
                "id": obj.get("id"),
                "title": obj.get("title") or obj.get("name"),
                "price": self._to_float(obj.get("price")),
                "currency": obj.get("currency", "USD"),
                "location": obj.get("location"),
                "source": obj.get("source"),
                "raw": obj,
            }

            # строгий MVP фильтр
            if not normalized["title"]:
                continue

            result.append(normalized)

        return result

    def _deduplicate(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.dedup_engine:
            return self.dedup_engine.merge(objects)

        return objects

    def _to_float(self, value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(str(value).replace(",", "."))
        except Exception:
            return None

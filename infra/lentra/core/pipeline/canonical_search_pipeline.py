from typing import Any, Dict, List, Optional


class CanonicalSearchPipeline:
    """
    v3 SINGLE SOURCE OF TRUTH pipeline.
    """

    def __init__(
        self,
        dedup_engine=None,
        market_engine=None,
        ranking_engine=None,
        intelligence_orchestrator=None,
        guard=None,
    ):
        self.dedup_engine = dedup_engine
        self.market_engine = market_engine
        self.ranking_engine = ranking_engine
        self.intelligence_orchestrator = intelligence_orchestrator
        self.guard = guard

    def run(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        if self.guard:
            self.guard.assert_canonical("canonical_pipeline_v3")

        objects = self._normalize(objects)
        objects = self._deduplicate(objects)

        # 🧠 INTELLIGENCE RESTORED HERE
        if self.intelligence_orchestrator:
            objects = self.intelligence_orchestrator.enrich(objects)

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

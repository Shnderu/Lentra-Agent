from typing import Dict, Any
from lentra.core.explanation.explanation_engine import ExplanationEngine


class SearchEngine:
    """
    VIETNAM SEARCH + EXPLANATION LAYER
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.explainer = ExplanationEngine()

    def search(self, query: Dict[str, Any]) -> Dict[str, Any]:

        all_items = self.pipeline.dump_all()

        results = []

        for item in all_items:
            if not self._match(item, query):
                continue

            shaped = self._shape(item)
            explanation = self.explainer.explain(item)

            results.append({
                **shaped,
                **explanation
            })

        return {
            "count": len(results),
            "results": results
        }

    def _match(self, item: Dict[str, Any], query: Dict[str, Any]) -> bool:

        if "city" in query:
            city = (item.get("location", {}).get("city") or "").lower()
            if query["city"].lower() not in city:
                return False

        if "max_price" in query:
            if item.get("price_vnd", 0) > query["max_price"]:
                return False

        if "property_type" in query:
            if item.get("property_type") != query["property_type"]:
                return False

        if "max_risk" in query:
            if item.get("risk_score", 0) > query["max_risk"]:
                return False

        return True

    def _shape(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": item.get("id"),
            "title": item.get("title"),
            "price_vnd": item.get("price_vnd"),
            "market_price": item.get("market_price"),
            "deviation_pct": item.get("deviation_pct"),
            "risk_score": item.get("risk_score"),
            "risk_level": item.get("risk_level"),
            "location": item.get("location"),
            "source": item.get("source")
        }

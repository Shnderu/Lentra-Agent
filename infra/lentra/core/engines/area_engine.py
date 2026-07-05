from typing import Dict, Any
from lentra.core.engines.base_engine import BaseEngine


class AreaEngine(BaseEngine):
    """
    Phase 3-ready stub.

    For now:
    - normalizes geo context
    - returns safe defaults
    """

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        query = ctx.get("query", "")

        return {
            "score": 0.5,
            "city": self._extract_city(query),
            "country": self._extract_country(query),
            "weights": {
                "expat_density": 0.5,
                "tourism": 0.5,
                "cost_index": 0.5,
            },
            "version": "geo_v1_fixed",
        }

    def _extract_city(self, query: str) -> str:
        if "da nang" in query.lower():
            return "da_nang"
        return "unknown"

    def _extract_country(self, query: str) -> str:
        if "vietnam" in query.lower() or "da nang" in query.lower():
            return "Vietnam"
        return "unknown"

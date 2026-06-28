from typing import Any, List, Dict

from lentra.core.market_intelligence.search.filters.filter import apply_filters
from lentra.core.market_intelligence.search.rankers.scorer import score_listing


class SearchEngine:
    """
    MVP Search Engine:
    - in-memory flow
    - no parser dependency (inline query handling)
    """

    def search(self, listings: List[Any], query: Dict[str, Any]) -> List[Any]:

        if listings is None:
            return []

        # 1. FILTER STEP
        filtered = apply_filters(listings, query)

        # 2. RANK STEP
        scored = []
        for item in filtered:
            score = score_listing(item, query)
            scored.append((score, item))

        # 3. SORT BY SCORE DESC
        scored.sort(key=lambda x: x[0], reverse=True)

        return [x[1] for x in scored]

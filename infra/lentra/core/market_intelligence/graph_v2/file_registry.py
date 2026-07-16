from __future__ import annotations

from typing import Dict, List


class GraphFileRegistry:
    """
    Maps graph nodes to canonical Market Intelligence files.

    Static architecture registry.
    No runtime imports.
    No legacy compatibility paths.
    """

    def __init__(self):

        self.node_to_files: Dict[str, List[str]] = {

            "risk_engine": [
                "lentra/core/market_intelligence/engines/risk_engine.py",
            ],

            "pricing_engine": [
                "lentra/core/market_intelligence/engines/pricing_engine.py",
            ],

            "ranking_engine": [
                "lentra/core/market_intelligence/ranking/unified_ranking_engine.py",
            ],

            "dedup_engine": [
                "lentra/core/market_intelligence/engines/dedup_engine.py",
                "lentra/core/market_intelligence/dedup/dedup_index.py",
            ],

            "area_engine": [
                "lentra/core/market_intelligence/area/area_engine.py",
                "lentra/core/market_intelligence/area/micro_market_engine.py",
            ],

        }

    def resolve(self, node_id: str) -> List[str]:
        return self.node_to_files.get(node_id, [])

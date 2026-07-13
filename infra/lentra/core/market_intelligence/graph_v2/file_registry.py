from __future__ import annotations

from typing import Dict, List


class GraphFileRegistry:
    """
    Maps graph nodes → file candidates.

    Deterministic architecture index.

    Contains only canonical Market Intelligence modules.
    """


    def __init__(self):

        self.node_to_files: Dict[str, List[str]] = {

            "risk_engine": [
                "lentra/core/market_intelligence/engines/risk_engine.py",
                "lentra/core/market_intelligence/risk/scam_engine.py",
            ],


            "pricing_engine": [
                "lentra/core/market_intelligence/pricing/engine.py",
                "lentra/core/market_intelligence/pricing/price_engine.py",
            ],


            "ranking_engine": [
                "lentra/core/market_intelligence/ranking/ranking_engine.py",
                "lentra/core/market_intelligence/ranking/unified_ranking_engine.py",
            ],


            "dedup_engine": [
                "lentra/core/market_intelligence/dedup/dedup_engine.py",
                "lentra/core/market_intelligence/dedup/dedup_index.py",
            ],


            "area_engine": [
                "lentra/core/market_intelligence/area/area_engine.py",
                "lentra/core/market_intelligence/area/micro_market_engine.py",
            ],

        }


    def resolve(
        self,
        node_id: str
    ) -> List[str]:

        return self.node_to_files.get(
            node_id,
            []
        )

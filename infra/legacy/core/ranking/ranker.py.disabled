from typing import List, Dict, Any


class Ranker:
    """
    LEGACY WRAPPER (v1 compatibility)
    """

    def rank(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(listings, key=lambda x: x.get("price", 0))


def rank_listings(listings, market_context=None):
    """
    HYBRID ENTRY POINT:
    - if market_context exists → v2 ranking
    - else → fallback v1
    """

    try:
        from lentra.core.v2.ranking.ranker_v2 import RankerV2

        if market_context:
            return RankerV2().rank(listings, market_context)

    except Exception as e:
        print("[RANKER V2 FALLBACK]", e)

    return Ranker().rank(listings)

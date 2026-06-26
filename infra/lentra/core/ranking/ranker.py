from typing import List, Dict, Any


class Ranker:
    """
    FINAL SCORING LAYER ONLY
    """

    def rank(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(listings, key=lambda x: x.get("price", 0))


def rank_listings(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Functional wrapper for pipeline compatibility
    """
    return Ranker().rank(listings)

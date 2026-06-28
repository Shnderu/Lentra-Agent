from typing import List, Dict, Any
from lentra.core.v2.models.listing import Listing


class RiskEngineV2:
    """
    V2 Anti-scam / risk scoring engine.

    INPUT: Listing objects only
    OUTPUT: enriched Listing objects
    """

    def score(self, listings: List[Listing], market_context: Dict[str, Any] = None) -> List[Listing]:

        for listing in listings:
            score = 0
            flags = []

            price = listing.price
            description = listing.description or ""

            # -----------------------------
            # Core heuristics
            # -----------------------------

            if price is None:
                score += 50
                flags.append("no_price")

            if price is not None and price < 200:
                score += 20
                flags.append("suspicious_low_price")

            if not description:
                score += 10
                flags.append("no_description")

            # -----------------------------
            # Duplicate signal
            # -----------------------------

            if listing.duplicates and len(listing.duplicates) > 0:
                score += 15
                flags.append("has_duplicates")

            # -----------------------------
            # Market deviation signal
            # -----------------------------

            if listing.market_deviation is not None:
                if abs(listing.market_deviation) > 30:
                    score += 25
                    flags.append("high_market_deviation")

            # -----------------------------
            # Final normalization
            # -----------------------------

            listing.risk_score = min(score, 100)
            listing.risk_flags = flags

        return listings


# Backward compatibility hook (optional import safety)
def score_risk_v2(listings: List[Listing], market_context: Dict[str, Any] = None):
    return RiskEngineV2().score(listings, market_context)

# ============================================================
# QUALITY ENGINE V16.3
# ============================================================

from lentra.rent.quality.scoring.source_reputation import get_source_score
from lentra.rent.quality.filters.noise_filter import noise_score
from lentra.rent.quality.filters.duplicate import duplicate_score


class QualityEngine:
    def __init__(self):
        self.seen = set()

    def score(self, listing: dict) -> dict:
        source = get_source_score(listing.get("source", "unknown"))
        noise = noise_score(listing)
        dup = duplicate_score(listing, self.seen)

        trust = (source * 0.5) + (100 - noise) * 0.3 + (100 - dup) * 0.2

        return {
            "listing_id": listing.get("id"),
            "trust_score": round(trust, 2),
            "source_score": source,
            "noise_score": noise,
            "duplicate_score": dup,
        }

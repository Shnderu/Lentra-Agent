from typing import List
from lentra.core.v2.models.listing import Listing


class DeduplicatorV2:
    """
    V2 dedup engine (baseline clustering).

    Goal:
    - detect duplicates
    - attach duplicate IDs to primary listing
    - keep model fully object-based
    """

    def deduplicate(self, listings: List[Listing]) -> List[Listing]:

        normalized = []

        for i, listing in enumerate(listings):
            listing.duplicates = []

            for other in listings:
                if listing.id == other.id:
                    continue

                # -----------------------------
                # Basic clustering heuristic (MVP)
                # -----------------------------
                same_title = (
                    listing.title
                    and other.title
                    and listing.title.strip().lower() == other.title.strip().lower()
                )

                same_price = listing.price == other.price
                same_city = listing.city == other.city

                if same_title and same_price and same_city:
                    listing.duplicates.append(other.id)

            normalized.append(listing)

        return normalized


# Compatibility wrapper (safe during migration)
def deduplicate_v2(listings: List[Listing]) -> List[Listing]:
    return DeduplicatorV2().deduplicate(listings)

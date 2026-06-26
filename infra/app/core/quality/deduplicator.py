from typing import List
from lentra.core.contracts.listing_dto import ListingDTO


class Deduplicator:

    def deduplicate(self, listings: List[ListingDTO]):

        seen = set()
        result = []

        for l in listings:

            if not l.title:
                continue

            key = (
                l.title.lower().strip(),
                l.city,
                l.price
            )

            # 🔥 stronger dedup key
            if key in seen:
                continue

            seen.add(key)
            result.append(l)

        return result

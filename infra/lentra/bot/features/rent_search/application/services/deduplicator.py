from typing import List

from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class RentDeduplicator:

    def deduplicate(
        self,
        items: List[RentSearchItem]
    ) -> List[RentSearchItem]:

        result = []
        seen = set()

        for item in items:

            key = (
                (item.title or "").strip().lower(),
                (item.city or "").strip().lower(),
                item.price_value
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result

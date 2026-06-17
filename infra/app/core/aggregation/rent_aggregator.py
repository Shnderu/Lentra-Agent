from typing import List
from app.core.contracts.listing_dto import ListingDTO
from app.core.contracts.response_dto import RentResponseDTO


class RentAggregator:
    """
    Собирает результаты из разных источников:
    - merge
    - deduplicate
    - rank (простая эвристика)
    """

    def aggregate(self, query: str, sources: List[List[ListingDTO]]) -> RentResponseDTO:
        flat = []

        # merge
        for source in sources:
            flat.extend(source)

        # deduplicate (по title + price)
        seen = set()
        unique = []

        for item in flat:
            key = (item.title, item.price, item.city)
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        # ranking (простая эвристика: дешевле выше)
        unique.sort(key=lambda x: (x.price or 10**9))

        return RentResponseDTO(
            query=query,
            listings=unique,
            total=len(unique)
        )

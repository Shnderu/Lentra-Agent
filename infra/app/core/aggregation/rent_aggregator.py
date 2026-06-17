from typing import List
from app.core.contracts.listing_dto import ListingDTO
from app.core.contracts.response_dto import RentResponseDTO


class RentAggregator:

    def aggregate(self, query: str, sources: List[List[ListingDTO]]) -> RentResponseDTO:

        flat = []
        for source in sources:
            flat.extend(source)

        # dedup
        seen = set()
        unique = []

        for item in flat:
            key = (item.title, item.price, item.city)
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        # ranking (cheap first)
        unique.sort(key=lambda x: x.price or 10**9)

        return RentResponseDTO(
            query=query,
            listings=unique,
            total=len(unique)
        )

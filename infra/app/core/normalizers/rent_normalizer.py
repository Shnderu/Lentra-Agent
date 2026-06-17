from typing import List, Dict
from app.core.contracts.listing_dto import ListingDTO


class RentNormalizer:
    """
    Приводит любые сырые ответы к ListingDTO
    """

    def normalize(self, raw: Dict, source: str) -> List[ListingDTO]:
        listings = []

        for item in raw.get("results", []):
            listings.append(
                ListingDTO(
                    title=item.get("title"),
                    price=item.get("price"),
                    city=item.get("city"),
                    source=source,
                    url=item.get("url")
                )
            )

        return listings

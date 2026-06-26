from dataclasses import dataclass
from typing import List, Optional
from lentra.core.contracts.listing_dto import ListingDTO


@dataclass
class RentResponseDTO:
    query: str
    listings: List[ListingDTO]
    total: int

    def to_dict(self):
        return {
            "query": self.query,
            "total": self.total,
            "listings": [
                {
                    "title": l.title,
                    "price": l.price,
                    "city": l.city,
                    "source": l.source,
                    "url": l.url
                }
                for l in self.listings
            ]
        }

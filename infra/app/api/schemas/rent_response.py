from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class ListingSchema:
    title: str
    price: Optional[int]
    city: Optional[str]
    source: Optional[str]
    url: Optional[str]


@dataclass
class RentResponseSchema:
    query: str
    total: int
    listings: List[ListingSchema]

    def to_dict(self):
        return asdict(self)

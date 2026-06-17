from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ListingDTO:
    title: str
    price: int
    city: Optional[str]
    source: str
    room_type: Optional[str] = None
    raw_score: Optional[float] = None

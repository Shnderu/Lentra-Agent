from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class RentQuery:
    city: str
    budget: Optional[int] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None


@dataclass
class RentListing:
    title: str
    price: int
    currency: str
    location: str
    source: str
    url: str


@dataclass
class RentResult:
    listings: List[RentListing]
    sources_used: List[str]
    meta: Dict[str, Any]

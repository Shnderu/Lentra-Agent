from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class RentalSearchRequest:
    query: Optional[str] = None
    city: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None


@dataclass
class RentalCard:
    title: str
    price: str
    city: str
    meta: Dict[str, Any]


@dataclass
class RentalSearchResult:
    cards: List[RentalCard]

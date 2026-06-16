from dataclasses import dataclass
from typing import List, Any, Optional


@dataclass
class RentSearchInput:
    query: Optional[str] = None
    city: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None


@dataclass
class RentSearchItem:
    title: str
    price: str
    city: str
    meta: dict


@dataclass
class RentSearchOutput:
    items: List[RentSearchItem]
    total: int

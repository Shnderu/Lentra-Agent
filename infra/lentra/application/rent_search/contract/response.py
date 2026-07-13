from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RentalCard:
    title: str
    price: str
    city: str
    meta: Dict[str, Any]


@dataclass
class RentalSearchResult:
    cards: List[RentalCard]

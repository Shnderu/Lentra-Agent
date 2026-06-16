from dataclasses import dataclass
from typing import List


@dataclass
class RentalCard:
    id: str
    title: str
    city: str
    price: str
    score: float = 0.0


@dataclass
class RentalSearchRequest:
    query: str


@dataclass
class RentalSearchResult:
    cards: List[RentalCard]
    message: str = ""

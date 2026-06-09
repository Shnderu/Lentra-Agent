from dataclasses import dataclass
from typing import List


@dataclass
class FlightSearchRequest:
    origin: str
    destination: str
    date: str
    user_id: int


@dataclass
class FlightItem:
    airline: str
    price: float
    from_airport: str
    to_airport: str
    date: str
    duration: str
    provider: str


@dataclass
class FlightSearchResponse:
    items: List[FlightItem]

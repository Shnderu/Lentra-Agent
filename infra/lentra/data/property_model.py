from dataclasses import dataclass
from typing import Optional

@dataclass
class PropertyListing:
    source: str
    external_id: str
    title: str
    price: int
    currency: str = "USD"
    city: str = "Vietnam"
    district: Optional[str] = None
    link: Optional[str] = None
    rooms: Optional[int] = None
    raw: dict = None

from dataclasses import dataclass
from typing import Optional


@dataclass
class NormalizedRentQuery:
    raw_text: str

    city: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None

    property_type: Optional[str] = None  # apartment / room / house

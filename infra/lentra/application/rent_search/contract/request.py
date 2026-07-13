from dataclasses import dataclass
from typing import Optional


@dataclass
class RentalSearchRequest:
    query: Optional[str] = None
    city: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None

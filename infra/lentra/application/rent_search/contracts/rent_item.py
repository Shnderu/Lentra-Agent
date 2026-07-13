from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class RentSearchItem:
    title: str
    price: str
    city: str

    country: Optional[str] = None
    currency: Optional[str] = None
    price_value: Optional[float] = None

    source: Optional[str] = None
    url: Optional[str] = None

    meta: Dict[str, Any] | None = None

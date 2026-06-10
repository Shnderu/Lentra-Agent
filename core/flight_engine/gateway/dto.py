from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class FlightOffer:
    origin: str
    destination: str
    date: str

    price: float
    currency: str

    duration: str
    airline: str
    provider: str

    raw: Optional[Dict[str, Any]] = None

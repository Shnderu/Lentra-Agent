from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FlightResult:
    origin: str
    destination: str
    price: int
    currency: str = "RUB"
    airline: str = "FlyRum Demo"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "origin": self.origin,
            "destination": self.destination,
            "price": self.price,
            "currency": self.currency,
            "airline": self.airline,
        }

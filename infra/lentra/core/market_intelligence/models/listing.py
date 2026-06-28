from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Listing:

    id: str

    title: str

    price: float

    source: str

    city: str = ""

    location: str = ""

    url: str = ""

    currency: str = "USD"

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "source": self.source,
            "city": self.city,
            "location": self.location,
            "url": self.url,
            "currency": self.currency,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            price=float(data.get("price", 0)),
            source=data.get("source", "unknown"),
            city=data.get("city", ""),
            location=data.get("location", ""),
            url=data.get("url", ""),
            currency=data.get("currency", "USD"),
            metadata=data.get("metadata", {}),
        )

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ListingDTO:
    id: str
    title: str
    price: float
    currency: str
    city: str
    location: str
    source: str

    @staticmethod
    def from_raw(data: Any) -> "ListingDTO":
        """
        HARD GUARD:
        принимает только dict-like вход.
        str / Listing object -> сразу нормализуем или падаем.
        """

        if data is None:
            raise ValueError("ListingDTO input is None")

        if isinstance(data, str):
            raise ValueError(f"Invalid Listing input (str): {data}")

        # dict-compatible extraction (без .get в runtime pipeline)
        if isinstance(data, dict):
            return ListingDTO(
                id=str(data.get("id", "")),
                title=str(data.get("title", "")),
                price=float(data.get("price", 0) or 0),
                currency=str(data.get("currency", "USD")),
                city=str(data.get("city", "")),
                location=str(data.get("location", "")),
                source=str(data.get("source", "unknown")),
            )

        # object fallback (только attribute-safe access)
        try:
            return ListingDTO(
                id=str(getattr(data, "id", "")),
                title=str(getattr(data, "title", "")),
                price=float(getattr(data, "price", 0) or 0),
                currency=str(getattr(data, "currency", "USD")),
                city=str(getattr(data, "city", "")),
                location=str(getattr(data, "location", "")),
                source=str(getattr(data, "source", "unknown")),
            )
        except Exception as e:
            raise ValueError(f"Unsupported Listing format: {type(data)} -> {e}")

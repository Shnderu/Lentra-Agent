from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ListingDTO:
    id: Optional[str]
    title: str
    location: str
    price: float
    currency: str = "USD"
    source: str = "unknown"
    raw: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_any(x: Any) -> "ListingDTO":

        # dict input
        if isinstance(x, dict):
            return ListingDTO(
                id=x.get("id"),
                title=x.get("title") or x.get("text") or x.get("raw", ""),
                location=_safe_location(x),
                price=float(x.get("price") or 0),
                currency=x.get("currency", "USD"),
                source=x.get("source", "unknown"),
                raw=x
            )

        # object input
        if hasattr(x, "__dict__"):
            d = vars(x)
            return ListingDTO.from_any(d)

        # string input
        if isinstance(x, str):
            return ListingDTO(
                id=None,
                title=x,
                location="",
                price=0.0,
                currency="USD",
                source="string",
                raw={"text": x}
            )

        # fallback hard safety
        return ListingDTO(
            id=None,
            title=str(x),
            location="",
            price=0.0,
            currency="USD",
            source="unknown",
            raw={"value": str(x)}
        )


def _safe_location(x: dict) -> str:
    loc = x.get("location")

    if isinstance(loc, dict):
        return loc.get("city") or loc.get("name") or ""

    if isinstance(loc, str):
        return loc

    return ""

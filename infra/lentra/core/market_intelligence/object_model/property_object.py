from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PropertyObject:
    """
    Canonical property entity for Market Intelligence.

    Represents a real-world property after:
    Listing normalization
    Deduplication
    Entity resolution

    Not a raw listing.
    Not a user search request.
    """

    id: str | None = None

    entity_id: str | None = None

    canonical_listing_id: str | None = None

    title: str = ""

    price: float | None = None

    currency: str = "VND"

    city: str | None = None

    district: str | None = None

    segment_key: str | None = None

    property_type: str | None = None

    location: dict[str, Any] | None = None

    source: str | None = None

    linked_listings: list[str] = field(
        default_factory=list
    )

    sources: list[str] = field(
        default_factory=list
    )

    duplicate_count: int = 0

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

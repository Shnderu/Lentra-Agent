from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Listing:
    """
    Unified V2 domain model for all pipeline stages.
    This replaces dict-based listings across the system.
    """

    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    city: Optional[str] = None
    location: Optional[str] = None

    price: Optional[float] = None
    currency: Optional[str] = None

    source: Optional[str] = None
    source_url: Optional[str] = None

    normalized_price: Optional[float] = None

    duplicates: List[str] = field(default_factory=list)

    market_price: Optional[float] = None
    market_deviation: Optional[float] = None

    risk_score: Optional[float] = None
    risk_flags: List[str] = field(default_factory=list)

    area_score: Optional[float] = None

    ai_score: Optional[Dict[str, Any]] = field(default_factory=dict)
    ranking_score: Optional[float] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------
    # Compatibility layer (critical for migration)
    # -----------------------------

    def get(self, key: str, default=None):
        """
        Temporary compatibility layer to prevent crashes
        during v1 → v2 migration.
        """
        return getattr(self, key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Listing back to dict (only for UX/output layer).
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "city": self.city,
            "location": self.location,
            "price": self.price,
            "currency": self.currency,
            "source": self.source,
            "source_url": self.source_url,
            "normalized_price": self.normalized_price,
            "duplicates": self.duplicates,
            "market_price": self.market_price,
            "market_deviation": self.market_deviation,
            "risk_score": self.risk_score,
            "risk_flags": self.risk_flags,
            "area_score": self.area_score,
            "ai_score": self.ai_score,
            "ranking_score": self.ranking_score,
            "metadata": self.metadata,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Listing":
        """
        Adapter for v1 fetchers / normalizers.
        """
        return Listing(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            city=data.get("city"),
            location=data.get("location"),
            price=data.get("price"),
            currency=data.get("currency"),
            source=data.get("source"),
            source_url=data.get("source_url"),
            normalized_price=data.get("normalized_price"),
            duplicates=data.get("duplicates", []) or [],
        )

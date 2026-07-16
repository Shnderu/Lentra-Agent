from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Property:
    """
    Canonical property intelligence contract.

    Single domain representation for:
    ingestion -> normalization -> intelligence -> API
    """

    id: Optional[str] = None

    title: str = ""

    description: str = ""

    city: str = ""
    district: Optional[str] = None

    price: Optional[float] = None
    currency: str = "USD"

    property_type: Optional[str] = None

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_m2: Optional[float] = None

    features: Dict[str, Any] = field(default_factory=dict)

    source: str = ""
    source_chat_id: Optional[str] = None
    source_message_id: Optional[str] = None

    raw_text: str = ""

    # Market Intelligence layer
    market_price: Optional[float] = None
    price_delta_percent: Optional[float] = None

    risk_score: Optional[float] = None

    duplicate_ids: List[str] = field(default_factory=list)

    area_score: Optional[float] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


__all__ = ["Property"]

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class PriceObservation:
    """
    Immutable price observation event.

    Represents one observed market price point.
    """

    listing_id: str

    price: float

    currency: str = "USD"

    city: str = "da_nang"

    area: Optional[Any] = None

    source: Optional[str] = None

    segment_key: Optional[str] = None

    district: Optional[str] = None

    property_type: Optional[str] = None

    observed_at: str = ""

    metadata: Dict[str, Any] | None = None


    def __post_init__(self):

        if not self.observed_at:
            self.observed_at = datetime.utcnow().isoformat()

        if self.metadata is None:
            self.metadata = {}


    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)

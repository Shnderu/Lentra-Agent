# ============================================================
# PATCH V16.1 - GEO EXTENSION
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class CanonicalListing:
    id: str
    title: str
    city: str
    price: float
    rooms: Optional[int]
    area: Optional[str]
    source: str

    # GEO (NEW)
    lat: Optional[float] = None
    lon: Optional[float] = None
    district: Optional[str] = None

    # normalization metadata
    original_id: str = ""
    source_weight: float = 1.0

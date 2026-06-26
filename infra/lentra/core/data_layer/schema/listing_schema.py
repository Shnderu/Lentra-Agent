from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class Location:
    country: str = "Vietnam"
    region: Optional[str] = None   # North / Central / South
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None


@dataclass
class Listing:
    """
    UNIFIED VIETNAM LISTING SCHEMA

    RULES:
    - no source-specific fields
    - no city-specific schemas
    - all normalization happens BEFORE core
    """

    # identity
    id: str
    source: str
    source_url: Optional[str] = None

    # core commercial data
    price_usd: Optional[float] = None
    currency_raw: Optional[str] = None

    # property
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[str] = None  # studio / apartment / villa / room

    size_m2: Optional[float] = None
    rooms: Optional[int] = None

    # location (VIETNAM STANDARDIZED)
    location: Location = Location()

    # metadata
    images: Optional[List[str]] = None
    contact: Optional[str] = None
    timestamp: Optional[str] = None

    # derived (filled later by intelligence layer, NOT ingestion)
    market_price_usd: Optional[float] = None
    risk_score: Optional[float] = None
    duplicates: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "source_url": self.source_url,
            "price_usd": self.price_usd,
            "currency_raw": self.currency_raw,
            "title": self.title,
            "description": self.description,
            "property_type": self.property_type,
            "size_m2": self.size_m2,
            "rooms": self.rooms,
            "location": {
                "country": self.location.country,
                "region": self.location.region,
                "city": self.location.city,
                "district": self.location.district,
                "address": self.location.address,
            },
            "images": self.images,
            "contact": self.contact,
            "timestamp": self.timestamp,
            "market_price_usd": self.market_price_usd,
            "risk_score": self.risk_score,
            "duplicates": self.duplicates,
        }

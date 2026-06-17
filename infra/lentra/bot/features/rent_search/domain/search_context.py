from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchContext:
    raw_query: str

    country: Optional[str] = None
    city: Optional[str] = None

    property_type: Optional[str] = None

    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    currency: Optional[str] = None

    bedrooms: Optional[int] = None

    pet_friendly: bool = False
    furnished: bool = False

    long_term: bool = False
    expat_mode: bool = True

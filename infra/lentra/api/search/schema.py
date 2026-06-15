from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchRequest:
    query: Optional[str] = None
    city: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None

    lat: Optional[float] = None
    lng: Optional[float] = None

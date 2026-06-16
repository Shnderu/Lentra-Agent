from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchContext:
    raw_query: str
    query: str
    city: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None

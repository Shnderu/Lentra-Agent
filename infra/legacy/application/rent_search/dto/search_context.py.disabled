from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchContext:
    """
    Единый контракт для всего rent_search.
    """

    raw_query: str
    query: str

    city: Optional[str] = None
    country: Optional[str] = None

    min_price: Optional[int] = None
    max_price: Optional[int] = None

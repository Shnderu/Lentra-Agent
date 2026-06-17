from dataclasses import dataclass
from typing import Optional


@dataclass
class ListingDTO:
    """
    Единый формат жилья внутри всей системы.
    Независим от источника (API / scraping / future sources)
    """

    title: str
    price: Optional[int]
    currency: str = "USD"

    city: Optional[str] = None
    source: Optional[str] = None

    url: Optional[str] = None

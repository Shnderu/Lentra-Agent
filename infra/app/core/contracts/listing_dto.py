from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ListingDTO:
    title: str
    price: Optional[int]
    city: Optional[str]
    source: Optional[str] = None
    available: bool = True
    timestamp: Optional[datetime] = None

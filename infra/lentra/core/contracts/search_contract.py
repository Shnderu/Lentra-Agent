from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Listing:
    price: float
    title: str
    city: str = ""


@dataclass
class SearchContract:
    listings: List[Listing]
    query_text: str
    metadata: Dict[str, Any] = None

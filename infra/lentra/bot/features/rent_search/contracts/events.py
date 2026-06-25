from dataclasses import dataclass
from typing import Optional


@dataclass
class RentEvent:
    event_type: str   # "impression" | "click"

    query: str
    city: Optional[str]

    item_title: str
    item_city: Optional[str]

    position: Optional[int] = None
    score: Optional[float] = None

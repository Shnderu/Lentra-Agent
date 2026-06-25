from dataclasses import dataclass
from typing import Optional


@dataclass
class RentEvent:
    event_type: str  # impression | click

    user_id: Optional[int]

    query: str
    city: Optional[str]

    item_title: Optional[str] = None
    item_city: Optional[str] = None

    position: Optional[int] = None

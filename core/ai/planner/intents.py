
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TravelIntent:
    origin: Optional[str]
    destination: Optional[str]
    date: Optional[str]
    budget: Optional[int]
    mode: str  # ai_planner / deal_search / route_search
    tags: List[str]

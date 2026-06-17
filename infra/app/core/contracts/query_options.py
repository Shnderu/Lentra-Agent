from dataclasses import dataclass
from typing import Optional


@dataclass
class QueryOptions:
    city: Optional[str] = None
    budget: Optional[int] = None

    limit: int = 10
    sort_by: str = "score"   # score | price
    offset: int = 0

from dataclasses import dataclass
from typing import Optional


@dataclass
class UXState:

    mode: str  # LIST | DETAIL | FILTER | EMPTY

    page: int
    selected_id: Optional[str]

    search_id: str

    has_next: bool = False
    has_prev: bool = False

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class SessionState:
    user_id: int

    search_id: str = ""

    query: str = ""
    page: int = 0

    results: List[dict] = field(default_factory=list)

    selected_id: Optional[str] = None

    mode: str = "LIST"

    # LEVEL 7
    filters: Dict = field(default_factory=dict)
    saved_searches: List[str] = field(default_factory=list)

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class SessionState:
    user_id: int

    search_id: str = ""
    query: str = ""

    # pagination
    page: int = 0
    page_size: int = 5

    results: List[dict] = field(default_factory=list)

    selected_id: Optional[str] = None

    mode: str = "LIST"

    # filters / personalization
    filters: Dict = field(default_factory=dict)

    saved_searches: List[str] = field(default_factory=list)

    # behavioral memory (LEVEL 12)
    viewed_items: List[str] = field(default_factory=list)
    clicked_items: List[str] = field(default_factory=list)

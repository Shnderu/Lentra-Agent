from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class SessionState:

    user_id: int

    search_id: str = ""
    query: str = ""
    page: int = 0

    # ❗ ТОЛЬКО IDS (не full objects)
    result_ids: List[str] = field(default_factory=list)

    selected_id: Optional[str] = None
    mode: str = "LIST"

    filters: Dict = field(default_factory=dict)
    saved_searches: List[str] = field(default_factory=list)

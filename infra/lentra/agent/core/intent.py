# ============================================================
# LENTRA AGENT INTENT MODEL V17.0
# ============================================================

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Intent:
    user_id: str
    goal: str  # rent_best / rent_cheapest / rent_fast / explore
    constraints: Dict[str, Any]

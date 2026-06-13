# ============================================================
# LENTRA STATE MODELS V16.5
# ============================================================

from dataclasses import dataclass, field
from typing import Dict, Any, List
import time


@dataclass
class UserSession:
    user_id: str
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SavedSearch:
    id: str
    user_id: str
    query: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    last_run: float = 0
    active: bool = True

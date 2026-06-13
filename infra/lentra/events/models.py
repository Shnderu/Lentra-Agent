# ============================================================
# LENTRA EVENT MODEL V16.6
# ============================================================

from dataclasses import dataclass
import time
from typing import Dict, Any


@dataclass
class Event:
    user_id: str
    event_type: str   # view / click / save / ignore
    listing_id: str
    timestamp: float = time.time()
    meta: Dict[str, Any] = None

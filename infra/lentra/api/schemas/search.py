# ============================================================
# LENTRA API SCHEMAS V16.4
# ============================================================

from typing import Optional


class SearchRequest:
    city: str
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    rooms: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    page: int = 1
    limit: int = 20

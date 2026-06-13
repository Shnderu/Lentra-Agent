# ============================================================
# API RESPONSE MODEL V16.4
# ============================================================

from typing import List, Dict, Any


class SearchResponse:
    items: List[Dict[str, Any]]
    total: int
    page: int
    limit: int
    filters: Dict[str, Any]

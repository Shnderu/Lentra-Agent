from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class PropertyResponse(BaseModel):
    id: int
    title: str
    price: float
    city: str
    rank_score: float


class SearchResponse(BaseModel):
    results: List[PropertyResponse]
    meta: Optional[Dict[str, Any]] = {}

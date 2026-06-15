from pydantic import BaseModel
from typing import Optional, List, Dict


class SearchRequest(BaseModel):
    query: str
    budget_max: Optional[float] = None


class PropertyDTO(BaseModel):
    id: int
    title: str
    price_vnd_mln: float
    area_m2: float
    city: str
    district: str
    pool: bool
    sea_view: bool
    score: float
    score_breakdown: Dict[str, float]


class SearchResponse(BaseModel):
    query: str
    results: List[PropertyDTO]

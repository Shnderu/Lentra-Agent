from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: Optional[str] = None
    city: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None

    lat: Optional[float] = None
    lng: Optional[float] = None

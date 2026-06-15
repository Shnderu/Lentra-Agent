from dataclasses import dataclass
from typing import List


@dataclass
class SearchRequestDTO:
    query: str
    budget_max: float | None = None


@dataclass
class ApartmentDTO:
    id: int
    title: str
    price_vnd_mln: float
    area_m2: float
    city: str
    district: str
    pool: bool
    sea_view: bool
    score: float


@dataclass
class SearchResponseDTO:
    query: str
    results: List[ApartmentDTO]

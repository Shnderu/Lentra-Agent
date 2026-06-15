from dataclasses import dataclass


@dataclass
class PropertyDTO:
    id: str  # stable id (backend or generated hash)
    title: str
    city: str
    district: str
    price_vnd_mln: float
    score: float
    pool: bool
    sea_view: bool

from dataclasses import dataclass
from typing import Optional


@dataclass
class MarketFeatureVector:
    id: str
    price: float
    currency: str

    city: str
    location: str
    source: str

    normalized_price: Optional[float] = None

    # derived features
    price_per_sqm: Optional[float] = None
    expat_density_score: Optional[float] = None
    noise_score: Optional[float] = None

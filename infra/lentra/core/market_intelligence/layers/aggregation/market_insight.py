from dataclasses import dataclass
from typing import Optional


@dataclass
class MarketInsight:
    id: str
    cluster_id: str

    price: float
    market_avg: float
    deviation: float

    signal: str
    risk: float

    verdict: str  # human readable AI output

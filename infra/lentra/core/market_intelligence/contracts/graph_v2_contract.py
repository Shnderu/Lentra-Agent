from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class GraphV2Input:
    query: str
    price: float
    market_price: float
    enabled: bool = False


@dataclass
class GraphV2Output:
    enabled: bool
    graph: Dict[str, Any]
    score: float

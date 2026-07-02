from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class EngineContextV3:
    """
    SINGLE CANONICAL CONTEXT OBJECT FOR ALL ENGINES
    """

    raw: Dict[str, Any]

    # normalized views
    query: str = ""
    price: float = 0.0
    market_price: float = 0.0

    meta: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.raw.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "price": self.price,
            "market_price": self.market_price,
            "meta": self.meta,
        }

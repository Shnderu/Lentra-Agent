from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class IntelligenceResult:
    """
    Unified Market Intelligence contract.

    Single object flowing through:
    pricing
    risk
    dedup
    area
    ranking
    decision
    """

    property_id: str

    price: float = 0

    market_price: float = 0

    pricing: Dict[str, Any] = field(
        default_factory=dict
    )

    risk: Dict[str, Any] = field(
        default_factory=dict
    )

    dedup: Dict[str, Any] = field(
        default_factory=dict
    )

    area: Dict[str, Any] = field(
        default_factory=dict
    )

    ranking: Dict[str, Any] = field(
        default_factory=dict
    )

    decision: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    def to_dict(self):

        return {
            "property_id": self.property_id,
            "price": self.price,
            "market_price": self.market_price,
            "pricing": self.pricing,
            "risk": self.risk,
            "dedup": self.dedup,
            "area": self.area,
            "ranking": self.ranking,
            "decision": self.decision,
            "metadata": self.metadata,
        }

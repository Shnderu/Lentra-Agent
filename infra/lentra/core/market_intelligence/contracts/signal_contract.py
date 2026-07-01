from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class SignalContract:
    """
    Unified contract for all Market Intelligence outputs.
    No logic, only structure normalization.
    """

    price: float
    market_price: float | None
    deviation_pct: float

    risk_level: str
    risk_score: float

    duplicates: int

    area_score: float
    internet_score: float
    noise_score: float

    verdict: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "price": self.price,
            "market_price": self.market_price,
            "deviation_pct": self.deviation_pct,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "duplicates": self.duplicates,
            "area_score": self.area_score,
            "internet_score": self.internet_score,
            "noise_score": self.noise_score,
            "verdict": self.verdict,
        }

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Signal:
    score: float
    confidence: float = 1.0
    source: str = "unknown"
    meta: Optional[Dict[str, Any]] = None


@dataclass
class SignalContract:
    """
    Canonical Market Intelligence signal representation.

    This becomes the ONLY supported structure across MI layer.
    """

    pricing: Signal
    risk: Signal
    area: Signal
    dedup: Signal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pricing": self._sig(self.pricing),
            "risk": self._sig(self.risk),
            "area": self._sig(self.area),
            "dedup": self._sig(self.dedup),
        }

    def _sig(self, s: Signal) -> Dict[str, Any]:
        return {
            "score": s.score,
            "confidence": s.confidence,
            "source": s.source,
            "meta": s.meta or {},
        }

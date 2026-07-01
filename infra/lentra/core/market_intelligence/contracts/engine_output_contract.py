from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EngineOutput:
    """
    Unified contract for all intelligence engines.
    """

    value: Any = None
    score: Optional[float] = None
    signals: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "score": self.score,
            "signals": self.signals or {},
            "meta": self.meta or {},
        }

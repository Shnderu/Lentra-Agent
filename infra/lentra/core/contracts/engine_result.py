from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class EngineResult:
    """
    Unified contract across ALL market intelligence engines.
    This is the ONLY valid output shape downstream.
    """

    score: float = 0.0
    deviation: float = 0.0
    signal: str = "hold"
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

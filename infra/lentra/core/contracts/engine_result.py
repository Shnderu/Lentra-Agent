from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class EngineResult:
    """
    Standardized engine output contract

    IMPORTANT:
    - every engine MUST return this structure (future enforcement)
    """

    engine_name: str
    data: Dict[str, Any]
    latency_ms: float = 0.0
    trace: Optional[Dict[str, Any]] = None

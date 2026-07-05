from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EngineContext:
    """
    Single source of truth for engine execution

    RULES:
    - immutable input payload
    - enriched step-by-step state
    - no positional arguments anywhere in system
    """

    payload: Dict[str, Any]
    signals: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

    request_id: Optional[str] = None
    trace_id: Optional[str] = None

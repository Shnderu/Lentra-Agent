import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RuntimeContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    trace_id: Optional[str] = None

    session_state: Dict[str, Any] = field(default_factory=dict)
    pipeline_state: Dict[str, Any] = field(default_factory=dict)

    meta: Dict[str, Any] = field(default_factory=dict)


def create_context(user_id: Optional[str] = None) -> RuntimeContext:
    return RuntimeContext(user_id=user_id)

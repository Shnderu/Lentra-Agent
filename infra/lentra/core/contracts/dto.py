from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RequestDTO:
    query: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class ResponseDTO:
    query: str
    results: Any
    meta: Optional[Dict[str, Any]] = None

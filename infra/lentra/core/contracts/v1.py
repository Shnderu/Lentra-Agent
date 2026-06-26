from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class FlowV1:
    text: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class IntentV1:
    type: str
    confidence: float
    raw: Optional[dict] = None


@dataclass
class ScenarioV1:
    name: str
    handler: str
    params: dict


@dataclass
class ResultV1:
    status: str
    data: dict
    meta: dict | None = None

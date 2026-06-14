from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class UXState:
    chat_id: int
    user_id: int
    screen: str = "property_list"
    data: Dict[str, Any] = field(default_factory=dict)

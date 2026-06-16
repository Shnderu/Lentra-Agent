from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class FeatureContext:
    """
    Unified runtime context for all features.
    """

    message: Any
    text: str = ""
    intent: Optional[str] = None
    meta: Dict[str, Any] = None

    def __post_init__(self):
        if self.meta is None:
            self.meta = {}

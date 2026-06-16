from dataclasses import dataclass
from typing import Any


@dataclass
class FeatureContext:
    """
    Shared context passed to all features.
    """

    message: Any
    text: str
    intent: str
    meta: dict

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseEngine(ABC):
    """
    Unified engine contract for Lentra v3.

    RULES:
    - NO __call__ usage
    - ALL engines MUST implement run(ctx)
    - ctx is immutable input dict
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    @abstractmethod
    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for engine.
        """
        raise NotImplementedError

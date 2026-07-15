from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseEngine(ABC):
    """
    Unified Market Intelligence Engine contract.

    RULES:
    - all canonical engines expose run(ctx)
    - ctx is input payload
    - engine returns intelligence result
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    @abstractmethod
    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseEngine(ABC):
    """
    Canonical Market Intelligence Engine Contract.

    Rules:
    - single execution entrypoint: run(ctx)
    - ctx is immutable input contract
    - engine returns enriched result dictionary
    - no evaluate()
    - no shared mutable accumulator
    """

    def __init__(
        self,
        config: Dict[str, Any] | None = None
    ):
        self.config = config or {}


    @abstractmethod
    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute intelligence transformation.
        """
        raise NotImplementedError()

from typing import Protocol, Dict, Any, runtime_checkable, Optional


@runtime_checkable
class EngineContract(Protocol):
    """
    Unified contract for all market intelligence engines.
    """

    def evaluate(
        self,
        payload: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Standard entrypoint for all engines.
        Must be deterministic and stateless.
        """
        ...

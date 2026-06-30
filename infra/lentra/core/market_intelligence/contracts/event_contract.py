from typing import Protocol, Dict, Any, runtime_checkable


@runtime_checkable
class MarketEventContract(Protocol):
    """
    Event bus contract:
    all events must follow unified schema
    """

    def emit(self, event_type: str, payload: Dict[str, Any]) -> None:
        ...

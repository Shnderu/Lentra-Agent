from typing import Protocol, Dict, Any


class EngineContract(Protocol):
    """
    Unified contract for ALL market intelligence engines.
    """

    def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        ...

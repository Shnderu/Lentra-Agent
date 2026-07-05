from typing import Protocol, Dict, Any


class EngineContract(Protocol):
    """
    Unified contract for ALL engines
    """

    name: str

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        ...

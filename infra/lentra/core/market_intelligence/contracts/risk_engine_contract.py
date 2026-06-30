from typing import Protocol, Dict, Any, runtime_checkable


@runtime_checkable
class RiskEngineContract(Protocol):
    """
    Risk Layer Contract:
    input: listing
    output: listing + risk_score + flags
    """

    def analyze(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        ...

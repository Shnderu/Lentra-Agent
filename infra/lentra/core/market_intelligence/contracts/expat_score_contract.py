from typing import Protocol, Dict, Any, runtime_checkable


@runtime_checkable
class ExpatScoreContract(Protocol):
    """
    Expat / livability scoring contract
    """

    def analyze(self, listing: Dict[str, Any]) -> float:
        ...

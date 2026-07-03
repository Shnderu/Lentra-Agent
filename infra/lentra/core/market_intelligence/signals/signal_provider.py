from typing import Dict, Any, Protocol


class SignalProvider(Protocol):
    """
    Unified interface for all Market Intelligence signal sources.
    """

    name: str

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must return normalized signal dict:
        {
            "score": float,
            "confidence": float,
            "meta": dict
        }
        """
        ...

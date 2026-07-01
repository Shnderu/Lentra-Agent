from typing import Any, Dict, Protocol


class MarketLayer(Protocol):
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must be PURE enrichment only.
        No side effects.
        No cross-layer calls.
        """
        ...

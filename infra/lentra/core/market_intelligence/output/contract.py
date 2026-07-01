from typing import Dict, Any


class MarketIntelligenceOutputContract:
    """
    Stable output contract for Market Intelligence Engine.
    """

    def __init__(self, ui: Dict[str, Any], api: Dict[str, Any], meta: Dict[str, Any]):
        self.ui = ui or {}
        self.api = api or {}
        self.meta = meta or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ui": self.ui,
            "api": self.api,
            "meta": self.meta
        }

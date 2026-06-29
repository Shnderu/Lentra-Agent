from typing import Protocol, Dict, Any
from lentra.core.market_intelligence.contracts.market_object import MarketObject


class MarketPlugin(Protocol):

    name: str

    def run(self, obj: MarketObject) -> MarketObject:
        ...

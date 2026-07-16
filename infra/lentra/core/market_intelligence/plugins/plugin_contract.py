from typing import Protocol, Dict, Any
from lentra.core.market_intelligence.contracts.market_object_contract import MarketObjectContract


class MarketPlugin(Protocol):

    name: str

    def run(self, obj: MarketObjectContract) -> MarketObjectContract:
        ...

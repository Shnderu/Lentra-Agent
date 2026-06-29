from typing import Protocol, Dict, Any
from lentra.core.market_intelligence.contracts.market_object_contract import MarketObjectContract


class EngineContract(Protocol):

    def process(self, listing: MarketObjectContract) -> MarketObjectContract:
        ...

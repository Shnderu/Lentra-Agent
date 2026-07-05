from typing import Any, Dict

from lentra.core.market_intelligence.engines.base_engine import BaseEngine
from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine
from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
from lentra.core.market_intelligence.engines.area_engine import AreaEngine
from lentra.core.market_intelligence.engines.signals_engine import SignalsEngine
from lentra.core.market_intelligence.engines.expat_engine import ExpatEngine


class EngineRegistry:
    def __init__(self) -> None:
        self._engines: Dict[str, BaseEngine] = {
            "pricing": PricingEngine(),
            "risk": RiskEngine(),
            "dedup": DedupEngine(),
            "area": AreaEngine(),
            "signals": SignalsEngine(),
            "expat": ExpatEngine(),
        }

    def get(self, name: str) -> BaseEngine:
        if name not in self._engines:
            raise KeyError(name)
        return self._engines[name]

    def list_engines(self) -> Dict[str, BaseEngine]:
        return self._engines

    def run(self, name: str, payload: Dict[str, Any]) -> Any:
        return self.get(name).run(payload)

from typing import Any, Dict

from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine
from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
from lentra.core.market_intelligence.engines.area_engine import AreaEngine
from lentra.core.market_intelligence.engines.signals_engine import SignalsEngine
from lentra.core.market_intelligence.engines.expat_engine import ExpatEngine


class EngineRegistry:
    def __init__(self) -> None:
        self._engines = {
            "pricing": PricingEngine(),
            "risk": RiskEngine(),
            "dedup": DedupEngine(),
            "area": AreaEngine(),
            "signals": SignalsEngine(),
            "expat": ExpatEngine(),
        }

    def get(self, name: str):
        if name not in self._engines:
            raise KeyError(name)
        return self._engines[name]

    def resolve(self, name: str):
        return self.get(name)

    def list_engines(self):
        return self._engines

    def run(self, name: str, payload: Dict[str, Any]):
        engine = self.get(name)

        # SAFE ADAPTER
        if hasattr(engine, "run"):
            return engine.run(payload)

        if hasattr(engine, "execute"):
            return engine.execute(payload)

        raise RuntimeError(f"Engine {name} has no run/execute method")

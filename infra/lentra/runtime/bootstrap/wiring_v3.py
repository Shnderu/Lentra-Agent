from typing import Dict, Any

from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine
from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.signals_engine import SignalsEngine
from lentra.core.market_intelligence.engines.area_engine import AreaEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine

from lentra.core.market_intelligence.registry.engine_registry_v3 import EngineRegistryV3


def build_engines() -> Dict[str, Any]:
    return {
        "pricing": PricingEngine(),
        "risk": RiskEngine(),
        "signals": SignalsEngine(),
        "area": AreaEngine(),
        "dedup": DedupEngine(),
    }


def build_registry_v3() -> EngineRegistryV3:
    engines = build_engines()
    return EngineRegistryV3(engines)

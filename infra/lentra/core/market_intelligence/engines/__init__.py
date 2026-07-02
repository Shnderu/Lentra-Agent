from .pricing_engine import PricingEngine
from .risk import RiskEngine as RiskEngineV3
from .signals import SignalsEngine as SignalsEngineV3
from .area import AreaEngine as AreaEngineV3
from .dedup import DedupEngine as DedupEngineV3


def build_engines():
    return {
        "pricing": PricingEngine(),
        "risk": RiskEngineV3(),
        "signals": SignalsEngineV3(),
        "area": AreaEngineV3(),
        "dedup": DedupEngineV3(),
    }

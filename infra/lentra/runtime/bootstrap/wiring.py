from lentra.core.market_intelligence.pricing.engine import PricingEngine
from lentra.core.market_intelligence.signal.signal_layer import SignalLayer
from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine

from lentra.core.market_intelligence.graph.intelligence_graph_runtime import IntelligenceGraphRuntime
from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway


def build_gateway():
    """
    SAFE DI CONTAINER (v2)
    - NO API imports
    - NO circular dependency risk
    """

    engines = {
        "pricing": PricingEngine(),
        "signal": SignalLayer(),
        "risk": RiskEngineV2(),
        "dedup": UnifiedDedupEngine(),
        "expat": ExpatScoreEngine(),
    }

    graph = IntelligenceGraphRuntime()

    gateway = IntelligenceGateway(
        engines=engines,
        graph=graph
    )

    return gateway

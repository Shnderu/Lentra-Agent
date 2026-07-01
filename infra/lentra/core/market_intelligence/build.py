from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway
from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine


def build_intelligence_gateway(orchestrator=None):
    gateway = IntelligenceGateway(orchestrator=orchestrator)

    engines = {
        "pricing": PricingEngine(),
        "dedup": UnifiedDedupEngine(),
        "risk": RiskEngineV2(),
        "expat": ExpatScoreEngine()
    }

    return gateway, engines

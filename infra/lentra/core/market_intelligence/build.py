from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway

from lentra.core.market_intelligence.signal.signal_layer import SignalLayer
from lentra.core.market_intelligence.pricing.engine import PricingEngine
from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine

# SAFE ADAPTER WRAP
from lentra.core.market_intelligence.contracts.pricing_adapter import PricingEngineAdapter


def build_intelligence_gateway():
    signal = SignalLayer()

    # WRAPPED (IMPORTANT FIX)
    pricing = PricingEngineAdapter(PricingEngine())

    risk = RiskEngineV2()
    dedup = UnifiedDedupEngine()
    expat = ExpatScoreEngine()

    engines = {
        "pricing": pricing,
        "signal": signal,
        "risk": risk,
        "dedup": dedup,
        "expat": expat,
    }

    gateway = IntelligenceGateway()

    return gateway, engines

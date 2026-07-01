from typing import Dict, Any

from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway

from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.risk.risk_engine_adapter import RiskEngineAdapter
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine


class MarketIntelligenceEngine:

    def __init__(self):
        self.gateway = IntelligenceGateway()

        self.engines = {
            "pricing": PricingEngine(),
            "risk": RiskEngineAdapter(),
            "expat": ExpatScoreEngine(),
            "dedup": UnifiedDedupEngine(),
        }

    def _run_core_graph(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.gateway.run(self.engines, payload)

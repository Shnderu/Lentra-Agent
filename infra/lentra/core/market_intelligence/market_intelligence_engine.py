from typing import Dict, Any

from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway

from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.risk.risk_engine_adapter import RiskEngineAdapter
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine

from lentra.core.market_intelligence.contracts.intelligence_result import IntelligenceResult


class MarketIntelligenceEngine:
    """
    Unified Market Intelligence Engine.

    Responsibility:

    - execute intelligence engines
    - normalize output
    - return single intelligence object

    Does NOT:
    - make final user decision
    - rank listings
    - replace Decision Layer
    """


    def __init__(self):

        self.gateway = IntelligenceGateway()

        self.engines = {

            "pricing": PricingEngine(),

            "risk": RiskEngineAdapter(),

            "expat": ExpatScoreEngine(),

            "dedup": UnifiedDedupEngine(),

        }



    def _run_core_graph(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        return self.gateway.run(
            self.engines,
            payload
        )



    def analyze(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        result = self._run_core_graph(
            payload
        )


        intelligence = IntelligenceResult(

            property_id=str(
                payload.get(
                    "id",
                    "unknown"
                )
            ),

            price=payload.get(
                "price",
                0
            ),

            market_price=payload.get(
                "market_price",
                0
            ),

            pricing=result.get(
                "pricing",
                {}
            ),

            risk=result.get(
                "risk",
                {}
            ),

            dedup=result.get(
                "dedup",
                {}
            ),

            area=result.get(
                "expat",
                {}
            ),

            metadata={

                "city": payload.get(
                    "city"
                ),

                "source": payload.get(
                    "source"
                )

            }

        )


        return intelligence.to_dict()

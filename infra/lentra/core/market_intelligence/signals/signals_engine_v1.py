from typing import Dict, Any

from lentra.core.market_intelligence.area.area_intelligence_adapter import (
    AreaIntelligenceAdapter
)

from lentra.core.market_intelligence.area.expat_area_intelligence_engine import (
    ExpatAreaIntelligenceEngine,
    AreaSignals
)


class SignalsEngineV1:
    """
    PURE SIGNAL LAYER

    RULES:
    - NO compute()
    - ONLY build()
    - NO side effects
    - deterministic extraction layer
    """

    name = "signals"


    def __init__(self):

        self.area_adapter = AreaIntelligenceAdapter()

        self.area_engine = ExpatAreaIntelligenceEngine()


    def build(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        price = float(
            payload.get(
                "price",
                0
            )
        )

        market_price = float(
            payload.get(
                "market_price",
                1
            )
        )


        deviation = abs(
            price - market_price
        ) / max(
            market_price,
            1
        )


        direction = (
            "over"
            if price > market_price
            else "under"
        )


        pricing = {

            "score":
                round(
                    min(
                        deviation,
                        1.0
                    ),
                    4
                ),

            "direction":
                direction,

            "deviation":
                round(
                    deviation,
                    4
                )
        }


        raw_area = payload.get(
            "area_intelligence"
        )


        if not raw_area:

            raw_area = self.area_engine.score(
                AreaSignals(
                    internet=8.5,
                    safety=7.0,
                    noise=6.5,
                    infrastructure=8.0,
                    expat_density=9.0,
                    walkability=7.0,
                    transport=7.0,
                    cafes=8.0,
                    coworking=8.0,
                    beach_distance=8.0
                )
            )


        area = self.area_adapter.build(
            payload,
            raw_area
        )


        dedup = {

            "score": 1.0,

            "confidence": 1.0

        }


        return {

            "pricing":
                pricing,

            "area":
                area,

            "dedup":
                dedup
        }

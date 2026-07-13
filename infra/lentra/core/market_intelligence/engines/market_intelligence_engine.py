from typing import Dict, Any

from lentra.core.market_intelligence.engines.base_engine import BaseEngine


class MarketIntelligenceEngine(BaseEngine):
    """
    Canonical Market Intelligence gateway engine.

    Responsibility:
    - interpret listing price against market truth
    - provide pricing signal
    - provide market deviation

    Business intelligence remains inside:
        market_service
        market_truth_engine
    """

    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:

        price = ctx.get(
            "price",
            0
        )

        market_price = ctx.get(
            "market_price",
            0
        )

        if market_price:

            difference = (
                price - market_price
            )

            difference_percent = (
                difference / market_price
            ) * 100

            deviation = abs(
                difference_percent
            ) / 100

        else:

            difference = 0
            difference_percent = 0
            deviation = 0


        if difference_percent > 5:

            verdict = "overpriced"

        elif difference_percent < -5:

            verdict = "good_deal"

        else:

            verdict = "market_price"


        return {

            "listing_price": price,

            "market_price": market_price,

            "difference": round(
                difference,
                2
            ),

            "difference_percent": round(
                difference_percent,
                2
            ),

            "verdict": verdict,

            "pricing_score": round(
                max(
                    0.0,
                    min(
                        1.0,
                        1 - deviation
                    )
                ),
                4
            ),

            "direction":
                "over"
                if difference > 0
                else "under",

            "confidence": 0.9,

            "version": "pricing_v3_product"
        }

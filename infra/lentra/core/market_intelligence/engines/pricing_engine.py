from typing import Dict, Any

from lentra.core.engines.base_engine import BaseEngine


class PricingEngine(BaseEngine):
    """
    Canonical Market Intelligence Pricing Engine.

    Contract:

        run(ctx) -> intelligence result
    """

    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:

        price = ctx.get(
            "price",
            0
        )

        market = ctx.get(
            "market_price",
            0
        )

        if market:

            deviation = (
                price - market
            ) / market

            score = 1 - abs(
                deviation
            )

            score = max(
                0.0,
                min(
                    1.0,
                    score
                )
            )

        else:

            deviation = 0
            score = 0.5


        return {
            **ctx,

            "pricing": {

                "price": price,

                "market_price": market,

                "score": round(
                    score,
                    4
                ),

                "delta": round(
                    price - market,
                    2
                ),

                "deviation": round(
                    deviation,
                    4
                ),

                "status": "ok"
            }
        }

from typing import Dict, Any

from lentra.core.engines.base_engine import BaseEngine


class PricingEngine(BaseEngine):
    """
    Canonical Market Intelligence Pricing Engine.

    Contract:

        run(ctx) -> intelligence result

    Output:
        - price comparison
        - market position
        - pricing signal
    """


    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:

        price = float(
            ctx.get(
                "price",
                0
            )
            or 0
        )


        market = float(
            ctx.get(
                "market_price",
                0
            )
            or 0
        )


        if market > 0:

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


            if deviation < -0.05:

                market_position = "below_market"

                pricing_signal = "good_deal"


            elif deviation > 0.05:

                market_position = "above_market"

                pricing_signal = "overpriced"


            else:

                market_position = "market_price"

                pricing_signal = "fair_price"


            percentile = round(
                50 + (
                    deviation * 100
                ),
                1
            )


            percentile = max(
                0,
                min(
                    100,
                    percentile
                )
            )


        else:

            deviation = 0

            score = 0.5

            market_position = "unknown"

            pricing_signal = "no_market_data"

            percentile = 50



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

                "market_position": market_position,

                "pricing_signal": pricing_signal,

                "market_percentile": percentile,

                "status": "ok"

            }

        }

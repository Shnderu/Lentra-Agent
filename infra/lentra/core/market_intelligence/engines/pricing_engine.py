from ._base import BaseEngine


class PricingEngine(BaseEngine):
    """
    V3 PRICE INTELLIGENCE ENGINE

    Responsibility:
    - compare listing price with market price
    - normalize deviation into 0..1 score
    - preserve market context for downstream AI layers
    """

    def evaluate(self, result, ctx=None):

        if not isinstance(result, dict):
            result = {}

        price = result.get(
            "price",
            0
        )

        market = result.get(
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


        result["pricing"] = {

            # keep original market context
            "price": price,

            "market_price": market,

            # intelligence metrics
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


        return result

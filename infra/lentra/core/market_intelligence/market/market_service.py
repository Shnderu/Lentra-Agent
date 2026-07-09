import statistics

from lentra.core.market_intelligence.market.market_snapshot import (
    MarketSnapshot
)


class MarketService:
    """
    Market Intelligence analytical layer.

    Converts raw normalized listings
    into MarketSnapshot.

    Future extensions:
    - district pricing
    - historical snapshots
    - market trends
    - liquidity
    - confidence calibration
    """


    def analyze(
        self,
        listings: list
    ) -> dict:

        prices = [
            item.get("price")
            for item in listings
            if item.get("price")
        ]


        if not prices:

            return MarketSnapshot(
                clean_listings=listings
            ).to_dict()


        median = statistics.median(
            prices
        )

        mean = statistics.mean(
            prices
        )


        sorted_prices = sorted(
            prices
        )


        q1 = sorted_prices[
            len(sorted_prices) // 4
        ]

        q3 = sorted_prices[
            (len(sorted_prices) * 3) // 4
        ]


        iqr = q3 - q1

        low = q1 - (
            1.5 * iqr
        )

        high = q3 + (
            1.5 * iqr
        )


        clean = []

        outliers = 0


        for item in listings:

            price = item.get(
                "price"
            )


            if price is None:
                continue


            if price < low or price > high:

                item["anomaly_flag"] = True

                item["risk_score_boost"] = 0.2

                outliers += 1

            else:

                item["anomaly_flag"] = False


            clean.append(
                item
            )


        confidence = min(
            len(prices) / 20,
            1.0
        )


        snapshot = MarketSnapshot(

            city="da_nang",

            median_price=median,

            mean_price=mean,

            q1=q1,

            q3=q3,

            sample_size=len(prices),

            outliers_detected=outliers,

            confidence=round(
                confidence,
                2
            ),

            price_min=min(prices),

            price_max=max(prices),

            market_health=(
                "stable"
                if len(prices) >= 5
                else "low_sample"
            ),

            clean_listings=clean

        )


        return snapshot.to_dict()

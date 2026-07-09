import statistics

from lentra.core.market_intelligence.repository.market_snapshot_repository import (
    MarketSnapshotRepository,
)


class MarketTruthEngine:

    def __init__(self):

        self.snapshot_repository = MarketSnapshotRepository()


    def stabilize(
        self,
        listings: list
    ) -> dict:

        prices = [
            l.get("price")
            for l in listings
            if l.get("price")
        ]


        if not prices:

            snapshot = {

                "median_price": None,

                "mean_price": None,

                "outliers_removed": 0,

                "clean_listings": listings

            }

            return snapshot


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


        low = q1 - 1.5 * iqr

        high = q3 + 1.5 * iqr


        clean = []

        outliers = 0


        for listing in listings:

            price = listing.get(
                "price"
            )


            if price is None:

                continue


            if price < low or price > high:

                listing["anomaly_flag"] = True

                listing["risk_score_boost"] = 0.2

                outliers += 1


            else:

                listing["anomaly_flag"] = False


            clean.append(
                listing
            )


        city = "unknown"

        if clean:

            city = clean[0].get(
                "city",
                "unknown"
            )


        snapshot = {

            "city": city,

            "median_price": median,

            "mean_price": mean,

            "q1": q1,

            "q3": q3,

            "outliers_removed": outliers,

            "clean_listings": clean

        }


        self.snapshot_repository.save(
            snapshot
        )


        return snapshot

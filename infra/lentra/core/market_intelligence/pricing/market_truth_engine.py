import statistics

from lentra.core.market_intelligence.repository.market_snapshot_repository import (
    MarketSnapshotRepository,
)


class MarketTruthEngine:
    """
    Market Truth Authority.

    Responsibility:
    - stabilize raw market prices
    - remove anomalies
    - produce canonical market snapshot

    Canonical price:
    - price_vnd

    Legacy:
    - price fallback only
    """

    def __init__(self):

        self.snapshot_repository = MarketSnapshotRepository()


    def _get_price(
        self,
        listing: dict
    ):

        if listing.get("price_vnd") is not None:

            return float(
                listing["price_vnd"]
            )

        if listing.get("price") is not None:

            return float(
                listing["price"]
            )

        return None


    def stabilize(
        self,
        listings: list
    ) -> dict:


        normalized = []


        for listing in listings:

            price = self._get_price(
                listing
            )

            if price is None:
                continue


            item = dict(
                listing
            )

            item["price_vnd"] = price

            normalized.append(
                item
            )


        prices = [
            item["price_vnd"]
            for item in normalized
        ]


        if not prices:

            snapshot = {

                "city": "unknown",

                "median_price": None,

                "mean_price": None,

                "price_min": None,

                "price_max": None,

                "q1": None,

                "q3": None,

                "sample_size": 0,

                "confidence": 0.0,

                "market_health": "unknown",

                "outliers_removed": 0,

                "clean_listings": []

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
            len(sorted_prices)//4
        ]


        q3 = sorted_prices[
            (len(sorted_prices)*3)//4
        ]


        iqr = q3 - q1


        low = q1 - (1.5 * iqr)

        high = q3 + (1.5 * iqr)


        clean = []

        outliers = 0


        for listing in normalized:

            price = listing["price_vnd"]


            if price < low or price > high:

                listing["anomaly_flag"] = True

                listing["risk_score_boost"] = 0.2

                outliers += 1

            else:

                listing["anomaly_flag"] = False


            clean.append(
                listing
            )


        clean_prices = [

            item["price_vnd"]

            for item in clean

            if not item.get(
                "anomaly_flag"
            )

        ]


        confidence = min(
            1.0,
            len(clean_prices)/20
        )


        if confidence >= 0.7:

            health = "stable"

        elif confidence >= 0.3:

            health = "limited"

        else:

            health = "weak"


        city = clean[0].get(
            "city",
            "unknown"
        )


        snapshot = {

            "city": city,

            "median_price": median,

            "mean_price": mean,

            "price_min": min(prices),

            "price_max": max(prices),

            "q1": q1,

            "q3": q3,

            "sample_size": len(clean_prices),

            "confidence": round(
                confidence,
                2
            ),

            "market_health": health,

            "outliers_removed": outliers,

            "clean_listings": clean

        }


        self.snapshot_repository.save(
            snapshot
        )


        return snapshot

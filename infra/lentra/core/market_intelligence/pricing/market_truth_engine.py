import statistics


class MarketTruthEngine:

    def __init__(self):
        pass

    def stabilize(self, listings: list) -> dict:

        prices = [l.get("price") for l in listings if l.get("price")]

        if not prices:
            return {
                "median_price": None,
                "mean_price": None,
                "outliers_removed": 0,
                "clean_listings": listings
            }

        median = statistics.median(prices)

        # robust bounds (IQR-lite approximation)
        sorted_prices = sorted(prices)
        q1 = sorted_prices[len(sorted_prices)//4]
        q3 = sorted_prices[(len(sorted_prices)*3)//4]

        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr

        clean = []
        outliers = 0

        for l in listings:
            p = l.get("price")

            if p is None:
                continue

            if p < low or p > high:
                l["anomaly_flag"] = True
                l["risk_score_boost"] = 0.2
                outliers += 1
            else:
                l["anomaly_flag"] = False

            clean.append(l)

        return {
            "median_price": median,
            "q1": q1,
            "q3": q3,
            "outliers_removed": outliers,
            "clean_listings": clean
        }

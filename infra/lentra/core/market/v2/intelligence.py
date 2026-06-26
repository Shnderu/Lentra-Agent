from typing import Dict, Any, List
import statistics


class MarketIntelligenceV2:
    """
    Market Intelligence v2:

    - медиана рынка
    - распределение цен
    - сегментация (cheap / normal / expensive)
    - отклонение от рынка
    """

    def analyze(self, listings: List[Dict[str, Any]], query: Dict[str, Any]) -> Dict[str, Any]:

        prices = [
            x.get("normalized_price") or x.get("price")
            for x in listings
            if x.get("price") is not None
        ]

        if not prices:
            return {
                "market_price": None,
                "segments": [],
                "note": "no data"
            }

        median_price = statistics.median(prices)

        q1 = self._percentile(prices, 25)
        q3 = self._percentile(prices, 75)

        current_budget = query.get("budget")

        return {
            "market_price": round(median_price, 2),
            "p25": round(q1, 2),
            "p75": round(q3, 2),
            "distribution": {
                "min": min(prices),
                "max": max(prices),
            },
            "segments": self._segment(listings, median_price, q1, q3),
            "budget_fit": self._budget_fit(current_budget, median_price) if current_budget else None
        }

    def _segment(self, listings, median, q1, q3):

        result = []

        for x in listings:
            price = x.get("normalized_price") or x.get("price")

            if price <= q1:
                label = "cheap"
            elif price <= q3:
                label = "normal"
            else:
                label = "expensive"

            result.append({
                **x,
                "market_segment": label
            })

        return result

    def _budget_fit(self, budget, median):

        deviation = ((budget - median) / median) * 100

        return {
            "budget": budget,
            "median": median,
            "deviation_pct": round(deviation, 2),
            "status": (
                "below_market" if deviation < -10 else
                "market" if abs(deviation) <= 10 else
                "above_market"
            )
        }

    def _percentile(self, data, percent):

        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * percent / 100
        f = int(k)
        c = min(f + 1, len(sorted_data) - 1)

        if f == c:
            return sorted_data[f]

        return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)

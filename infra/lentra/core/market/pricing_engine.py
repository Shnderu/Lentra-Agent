from typing import List, Dict, Any
from collections import defaultdict


class PricingEngine:
    """
    VIETNAM MARKET PRICING ENGINE

    Purpose:
    - estimate fair market price
    - compute deviation
    - build simple market bands
    """

    def build_market(self, clusters: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        clusters = dedup output
        """

        market = defaultdict(list)

        # 1. aggregate prices by location key
        for cluster in clusters:
            for item in cluster:
                key = self._market_key(item)
                price = item.get("price_vnd") or 0

                if price > 0:
                    market[key].append(price)

        # 2. compute stats
        result = {}

        for key, prices in market.items():
            if not prices:
                continue

            prices_sorted = sorted(prices)

            median = self._median(prices_sorted)
            avg = sum(prices) / len(prices)

            result[key] = {
                "median": median,
                "avg": avg,
                "min": prices_sorted[0],
                "max": prices_sorted[-1],
                "count": len(prices_sorted)
            }

        return result

    def score(self, item: Dict[str, Any], market_stats: Dict[str, Any]) -> Dict[str, Any]:
        key = self._market_key(item)
        price = item.get("price_vnd") or 0

        stats = market_stats.get(key)

        if not stats or price == 0:
            return {
                "market_price": None,
                "deviation_pct": None
            }

        market_price = stats["median"]
        deviation = ((price - market_price) / market_price) * 100

        return {
            "market_price": market_price,
            "deviation_pct": round(deviation, 2)
        }

    # -------------------------
    # INTERNALS
    # -------------------------

    def _market_key(self, item: Dict[str, Any]) -> str:
        location = item.get("location", {})
        city = (location.get("city") or "").lower()
        district = (location.get("district") or "").lower()

        return f"{city}:{district}"

    def _median(self, arr: List[float]) -> float:
        n = len(arr)
        mid = n // 2

        if n % 2 == 0:
            return (arr[mid - 1] + arr[mid]) / 2

        return arr[mid]


    def evaluate(self, payload):
        return self.score(payload)

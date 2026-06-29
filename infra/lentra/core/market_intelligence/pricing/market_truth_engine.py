from collections import defaultdict
import statistics


class MarketTruthEngine:
    """
    Lightweight market distribution tracker (MVP).

    Purpose:
    - build per-area price distribution
    - compute median / expected market price
    - provide deviation signal for scoring layer
    """

    def __init__(self):
        # area -> list of prices
        self.price_map = defaultdict(list)

    # -----------------------------
    # ingestion
    # -----------------------------
    def update(self, listing: dict):
        """
        Register listing into market distribution
        """
        area = listing.get("location") or "unknown"
        price = listing.get("price")

        if price is None:
            return

        try:
            price = float(price)
        except Exception:
            return

        self.price_map[area].append(price)

    # -----------------------------
    # market estimation
    # -----------------------------
    def get_market_price(self, listing: dict) -> float:
        """
        Returns median market price for area
        fallback → global median or fixed anchor
        """

        area = listing.get("location") or "unknown"

        prices = self.price_map.get(area, [])

        if len(prices) >= 3:
            return float(statistics.median(prices))

        # fallback stage (cold start)
        all_prices = []
        for v in self.price_map.values():
            all_prices.extend(v)

        if len(all_prices) >= 5:
            return float(statistics.median(all_prices))

        # global anchor (bootstrapping)
        return 500.0

    # -----------------------------
    # deviation signal
    # -----------------------------
    def price_deviation(self, listing: dict) -> float:
        """
        Normalized deviation from market price
        """

        price = listing.get("price") or 0
        try:
            price = float(price)
        except Exception:
            return 0.0

        market = self.get_market_price(listing)

        if market <= 0:
            return 0.0

        return (price - market) / market

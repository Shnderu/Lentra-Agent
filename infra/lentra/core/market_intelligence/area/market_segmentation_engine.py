import re
from collections import defaultdict


class MarketSegmentationEngine:
    """
    Lightweight geo-market segmentation (Vietnam MVP).

    Goal:
    - unify pricing context across cities
    - split market into interpretable segments
    - provide baseline grouping for MarketTruthEngine
    """

    def __init__(self):
        # segment -> list of prices
        self.segment_prices = defaultdict(list)

    # -------------------------
    # SEGMENT DETECTION
    # -------------------------
    def detect_segment(self, listing: dict) -> str:
        location = (listing.get("location") or "").lower()

        # coastal premium zones
        if any(x in location for x in ["beach", "my khe", "nha trang", "phu quoc"]):
            return "coastal_premium"

        # major expat cities
        if any(x in location for x in ["ho chi minh", "saigon", "hanoi"]):
            return "major_city"

        # mid-tier tourist cities
        if any(x in location for x in ["da nang", "hoi an", "hue"]):
            return "mid_tier_city"

        # fallback
        return "unknown"

    # -------------------------
    # INGESTION
    # -------------------------
    def update(self, listing: dict):
        segment = self.detect_segment(listing)
        price = listing.get("price")

        if price is None:
            return segment

        try:
            price = float(price)
        except Exception:
            return segment

        self.segment_prices[segment].append(price)

        return segment

    # -------------------------
    # BASELINE
    # -------------------------
    def get_baseline(self, listing: dict) -> float:
        segment = self.detect_segment(listing)

        prices = self.segment_prices.get(segment, [])

        if len(prices) >= 3:
            return float(sorted(prices)[len(prices) // 2])

        # global fallback
        all_prices = []
        for v in self.segment_prices.values():
            all_prices.extend(v)

        if len(all_prices) >= 5:
            return float(sorted(all_prices)[len(all_prices) // 2])

        return 500.0

    # -------------------------
    # DEVIATION
    # -------------------------
    def deviation(self, listing: dict) -> float:
        price = listing.get("price") or 0

        try:
            price = float(price)
        except Exception:
            return 0.0

        baseline = self.get_baseline(listing)

        if baseline <= 0:
            return 0.0

        return (price - baseline) / baseline

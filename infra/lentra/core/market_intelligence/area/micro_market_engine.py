from collections import defaultdict
from lentra.core.market_intelligence.area.temporal_market_engine import TemporalMarketEngine


class MicroMarketEngine:

    def __init__(self):
        self.temporal = TemporalMarketEngine()
        self.key_builder = lambda l, c: f"{c}:{self._cluster(l)}"

    def _cluster(self, listing: dict) -> str:
        location = (listing.get("location") or "").lower()

        if any(x in location for x in ["beach", "my khe", "an thuong"]):
            return "beach_zone"

        if any(x in location for x in ["center", "district", "tay ho"]):
            return "expat_hub"

        if any(x in location for x in ["old town", "hoi an"]):
            return "tourist_core"

        return "local"

    def detect_cluster(self, listing: dict, segment: str) -> str:
        return f"{segment}:{self._cluster(listing)}"

    def update(self, listing: dict):
        price = listing.get("price")
        segment = listing.get("segment") or "unknown"

        cluster = self.detect_cluster(listing, segment)

        if price is None:
            return cluster

        try:
            price = float(price)
        except Exception:
            return cluster

        self.temporal.update(cluster, price)

        listing["cluster_key"] = cluster
        return cluster

    def deviation(self, listing: dict):
        price = listing.get("price") or 0
        segment = listing.get("segment") or "unknown"
        cluster = self.detect_cluster(listing, segment)

        try:
            price = float(price)
        except Exception:
            return 0.0

        return self.temporal.deviation(cluster, price)

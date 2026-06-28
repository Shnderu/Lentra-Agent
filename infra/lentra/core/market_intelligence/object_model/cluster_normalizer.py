
import hashlib


class ClusterNormalizer:

    def normalize(self, cluster):

        listings = cluster.get("listings", [])

        prices = [l.get("price") for l in listings if l.get("price")]

        cluster_id = cluster.get("cluster_id") or self._make_cluster_id(listings)

        return {
            "cluster_id": cluster_id,
            "primary_id": self._primary_id(listings),
            "market_price": self._avg(prices),
            "listings": listings,
            "risk": cluster.get("risk", 0.5),
            "area_score": cluster.get("area_score", {})
        }

    def _avg(self, arr):

        return sum(arr) / len(arr) if arr else None

    def _primary_id(self, listings):

        if listings:
            return listings[0].get("id", "unknown")

        return "unknown"

    def _make_cluster_id(self, listings):

        raw = "".join([l.get("id", "") for l in listings])

        return hashlib.md5(raw.encode()).hexdigest()[:12]

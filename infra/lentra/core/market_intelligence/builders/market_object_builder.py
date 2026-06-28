from lentra.core.market_intelligence.models.listing import Listing
from lentra.core.market_intelligence.models.market_object import MarketObject


class MarketObjectBuilder:

    def build(self, cluster: dict) -> MarketObject:

        listings = []

        for item in cluster.get("listings", []):

            listings.append(
                Listing.from_dict(item)
            )

        if not listings and cluster.get("id"):

            listings.append(
                Listing.from_dict(cluster)
            )

        object_id = (
            cluster.get("cluster_id")
            or cluster.get("id")
            or "unknown"
        )

        obj = MarketObject(
            id=object_id
        )

        for listing in listings:
            obj.add_listing(listing)

        obj.market_price = cluster.get(
            "market_price",
            cluster.get("price")
        )

        obj.median_price = cluster.get(
            "median_price",
            obj.market_price
        )

        obj.price_deviation = cluster.get(
            "price_deviation"
        )

        obj.confidence = cluster.get(
            "confidence",
            0.0
        )

        obj.risk = cluster.get(
            "risk",
            0.5
        )

        area = cluster.get("area_score")

        if isinstance(area, dict):
            obj.area_score = area.get(
                "area_score",
                0.0
            )
        elif isinstance(area, (int, float)):
            obj.area_score = area

        obj.negotiation = cluster.get(
            "negotiation",
            {}
        )

        obj.verdict = cluster.get(
            "verdict",
            "neutral"
        )

        obj.history = cluster.get(
            "history",
            []
        )

        return obj

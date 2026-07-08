from lentra.core.market_intelligence.object_model.property_object import (
    PropertyObject,
)

from lentra.core.market_intelligence.builders.market_object_builder import (
    MarketObjectBuilder,
)


class PropertyMarketMapper:
    """
    Converts canonical PropertyObject entity
    into runtime MarketObject.

    Flow:

    EntityResolver
          |
          v
    PropertyObject
          |
          v
    MarketObject
    """

    def __init__(self):

        self.builder = MarketObjectBuilder()


    def to_market_object(
        self,
        property_object: PropertyObject
    ):

        cluster = {

            "cluster_id":
                property_object.entity_id
                or property_object.id
                or "unknown",

            "id":
                property_object.canonical_listing_id,

            "title":
                property_object.title,

            "price":
                property_object.price,

            "currency":
                property_object.currency,

            "city":
                property_object.city,

            "location":
                property_object.location,

            "confidence":
                property_object.confidence,

            "risk":
                property_object.metadata.get(
                    "risk",
                    0.5
                ),

            "listings": [],

            "sources":
                property_object.sources,

            "duplicate_count":
                property_object.duplicate_count,

            "entity_id":
                property_object.entity_id,

        }

        return self.builder.build(
            cluster
        )

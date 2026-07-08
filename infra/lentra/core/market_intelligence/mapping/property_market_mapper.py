from lentra.core.market_intelligence.object_model.property_object import PropertyObject
from lentra.core.market_intelligence.models.market_object import MarketObject
from lentra.core.market_intelligence.models.listing import Listing


class PropertyMarketMapper:
    """
    Converts resolved PropertyObject entity
    into Market Intelligence MarketObject.

    PropertyObject:
        canonical real-world property entity

    MarketObject:
        intelligence-ready representation
    """

    def map(
        self,
        property_object: PropertyObject
    ) -> MarketObject:

        listing = Listing(
            id=(
                property_object.canonical_listing_id
                or property_object.entity_id
                or "unknown"
            ),
            title=property_object.title,
            price=float(
                property_object.price or 0
            ),
            source=(
                property_object.source
                or "unknown"
            ),
            city=(
                property_object.city
                or ""
            ),
            location=(
                property_object.location
                or ""
            ),
            currency=property_object.currency,
            metadata={
                **property_object.metadata,
                "entity_id": property_object.entity_id,
                "linked_listings": property_object.linked_listings,
                "sources": property_object.sources,
                "duplicate_count": property_object.duplicate_count,
            }
        )

        return MarketObject(
            id=(
                property_object.entity_id
                or property_object.id
                or "unknown"
            ),
            listings=[
                listing
            ],
            market_price=property_object.price,
            median_price=property_object.price,
            confidence=property_object.confidence,
        )

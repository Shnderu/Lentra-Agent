from lentra.core.contracts.v1.listing_dto import ListingDTO
from lentra.core.market_intelligence.features.feature_vector import MarketFeatureVector


def to_feature_vector(dto: ListingDTO) -> MarketFeatureVector:
    """
    Единственная точка превращения рынка в ML-ready структуру
    """

    return MarketFeatureVector(
        id=dto.id,
        price=dto.price,
        currency=dto.currency,
        city=dto.city,
        location=dto.location,
        source=dto.source,
        normalized_price=_normalize_price(dto.price, dto.currency),
    )


def _normalize_price(price: float, currency: str) -> float:
    # MVP: фиксируем USD
    if currency == "USD":
        return float(price)

    # future FX layer
    return float(price)

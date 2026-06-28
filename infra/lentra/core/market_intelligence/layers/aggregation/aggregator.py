
from lentra.core.market_intelligence.layers.aggregation.market_insight import MarketInsight


def build_insight(listing, cluster_id, price_signal, stats) -> MarketInsight:

    market_avg = price_signal.get("market_avg", listing.price)

    deviation = (listing.price - market_avg) / market_avg if market_avg else 0

    signal = price_signal.get("signal")
    risk = price_signal.get("risk")

    if signal == "cheap":
        verdict = "below market — good deal"
    elif signal == "expensive":
        verdict = "above market — overpay risk"
    else:
        verdict = "market aligned — acceptable"

    return MarketInsight(
        id=listing.id,
        cluster_id=cluster_id,
        price=listing.price,
        market_avg=market_avg,
        deviation=deviation,
        signal=signal,
        risk=risk,
        verdict=verdict
    )

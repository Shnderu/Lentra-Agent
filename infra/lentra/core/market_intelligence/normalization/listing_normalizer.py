

from lentra.core.market_intelligence.features.feature_mapper import to_feature_vector


def normalize_listing(l: dict):

    if not l:
        return {}

    listing_id = l.get("id")

    price = l.get("price")
    if isinstance(price, dict):
        price = price.get("value")

    try:
        price = float(price)
    except:
        price = 0.0

    features = to_feature_vector(l)

    return {
        "id": listing_id,
        "title": l.get("title", ""),
        "city": l.get("city", ""),
        "cluster_id": l.get("cluster_id"),
        "price": price,
        "features": features["features"],
        "signals": l.get("signals", {}),
        "raw": l
    }



def compute_rank(insight, similar_listings: list) -> dict:
    """
    insight: MarketInsight
    similar_listings: list of MarketInsight-like dicts
    """

    if not similar_listings:
        return {
            "rank": 1,
            "percentile": 1.0,
            "comment": "single listing in cluster"
        }

    prices = [x["price"] for x in similar_listings if "price" in x]

    if not prices:
        return {
            "rank": 1,
            "percentile": 1.0,
            "comment": "no comparable data"
        }

    sorted_prices = sorted(prices)

    rank = sorted_prices.index(insight.price) + 1 if insight.price in sorted_prices else len(sorted_prices)

    percentile = 1 - (rank / len(sorted_prices))

    return {
        "rank": rank,
        "percentile": round(percentile, 2),
        "cluster_size": len(sorted_prices)
    }



def compute_cluster_stats(listings):

    prices = [l["price"] for l in listings if isinstance(l.get("price"), (int, float))]

    if not prices:
        return {
            "avg": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "count": 0
        }

    prices_sorted = sorted(prices)

    return {
        "avg": sum(prices) / len(prices),
        "median": prices_sorted[len(prices)//2],
        "min": min(prices),
        "max": max(prices),
        "count": len(prices)
    }

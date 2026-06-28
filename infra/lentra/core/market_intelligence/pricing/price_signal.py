

def compute_price_signal(price, cluster_stats):

    if not cluster_stats or cluster_stats["avg"] == 0:
        return {
            "signal": "unknown",
            "deviation": 0.0
        }

    avg = cluster_stats["avg"]

    deviation = (price - avg) / avg

    if deviation < -0.15:
        signal = "cheap"
    elif deviation > 0.15:
        signal = "expensive"
    else:
        signal = "neutral"

    return {
        "signal": signal,
        "deviation": deviation
    }

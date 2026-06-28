

def compute_price_signal(price: float, stats: dict) -> dict:
    avg = stats.get("avg_price", price)

    deviation = (price - avg) / avg if avg else 0

    if deviation < -0.1:
        signal = "cheap"
        risk = 0.3
    elif deviation > 0.15:
        signal = "expensive"
        risk = 0.7
    else:
        signal = "neutral"
        risk = 0.5

    return {
        "market_avg": avg,
        "signal": signal,
        "risk": risk
    }

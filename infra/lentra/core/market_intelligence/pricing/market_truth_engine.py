

def compute_market_truth(listing: dict) -> dict:

    price = listing.get("price", 0)
    market_avg = listing.get("market_avg", price)

    if not market_avg:
        market_avg = price

    deviation = (price - market_avg) / market_avg if market_avg else 0

    if deviation < -0.1:
        verdict = "undervalued"
    elif deviation > 0.1:
        verdict = "overpriced"
    else:
        verdict = "market aligned"

    return {
        "price": price,
        "market_avg": market_avg,
        "deviation": round(deviation, 4),
        "verdict": verdict
    }


def estimate_market_price(listings, query):
    prices = [l["normalized_price"] for l in listings]
    if not prices:
        return {"market_price": None}

    avg = sum(prices) / len(prices)

    return {
        "market_price": round(avg, 2)
    }

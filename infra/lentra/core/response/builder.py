
def build_response(listings, market, query):
    return {
        "city": query.get("city"),
        "market_price": market.get("market_price"),
        "listings": listings,
        "summary": {
            "total": len(listings),
            "note": "MVP pipeline output"
        }
    }

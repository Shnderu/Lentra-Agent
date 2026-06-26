from typing import List
from lentra.core.models.listing import Listing


def estimate_market_price(query: dict, listings: List[Listing]) -> dict:

    if not listings:
        return {
            "market_price": None,
            "note": "no listings"
        }

    prices = [l.normalized_price for l in listings if l.normalized_price]

    if not prices:
        return {
            "market_price": None,
            "note": "empty prices"
        }

    market_price = sum(prices) / len(prices)

    return {
        "market_price": round(market_price, 2)
    }

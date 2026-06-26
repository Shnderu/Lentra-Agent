from typing import List, Dict
from lentra.core.models.listing import Listing
from lentra.core.market.vietnam_market import build_market_index


def estimate_market_price(query: dict, listings: List[Listing]) -> dict:

    if not listings:
        return {"market_price": None, "note": "no listings"}

    market_index = build_market_index(listings)

    # fallback: global avg
    prices = [l.normalized_price for l in listings if l.normalized_price]

    global_avg = round(sum(prices) / len(prices), 2) if prices else None

    return {
        "market_price": global_avg,
        "market_index": market_index
    }

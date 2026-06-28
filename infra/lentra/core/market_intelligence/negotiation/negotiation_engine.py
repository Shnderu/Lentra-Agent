

def compute_negotiation_strategy(listing: dict, market: dict) -> dict:

    price = listing.get("price", 0)
    market_avg = market.get("market_avg", price)

    if market_avg == 0:
        market_avg = price

    overpay = (price - market_avg) / market_avg

    # потенциал торга
    if overpay > 0.15:
        discount_potential = 0.12
        strategy = "aggressive_negotiation"
    elif overpay > 0.05:
        discount_potential = 0.07
        strategy = "standard_negotiation"
    else:
        discount_potential = 0.03
        strategy = "low_room_for_negotiation"

    target_price = price * (1 - discount_potential)

    return {
        "strategy": strategy,
        "discount_potential": round(discount_potential, 4),
        "target_price": round(target_price, 2),
        "market_position": round(overpay, 4)
    }

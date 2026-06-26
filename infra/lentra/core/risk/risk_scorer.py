from lentra.core.models.listing import Listing


def score_risk(listings: list, market: dict) -> list:

    global_price = market.get("market_price") or 0

    for l in listings:

        score = 0
        flags = []

        if not l.price:
            score += 50
            flags.append("no_price")

        if l.price and l.price < 200:
            score += 20
            flags.append("suspicious_low_price")

        if global_price and l.price:
            deviation = ((l.price - global_price) / global_price) * 100
            l.market_deviation = round(deviation, 2)

        l.risk_score = score
        l.risk_flags = flags
        l.risk_level = (
            "low" if score < 30 else
            "medium" if score < 70 else
            "high"
        )

    return listings

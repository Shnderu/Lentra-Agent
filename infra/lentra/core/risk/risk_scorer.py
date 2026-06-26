from lentra.core.models.listing import Listing


def score_risk(listings: list, market: dict) -> list:

    market_price = market.get("market_price") or 0

    for l in listings:

        score = 0
        flags = []

        if not l.price:
            score += 50
            flags.append("no_price")

        if l.price and l.price < 200:
            score += 20
            flags.append("suspicious_low_price")

        if market_price and l.price:
            deviation = ((l.price - market_price) / market_price) * 100
            l.market_deviation = round(deviation, 2)

        if score > 100:
            score = 100

        l.risk_score = score
        l.risk_flags = flags
        l.risk_level = (
            "low" if score < 30 else
            "medium" if score < 70 else
            "high"
        )

    return listings

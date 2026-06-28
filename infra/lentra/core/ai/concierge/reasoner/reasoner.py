

def _get_price(listing: dict):

    price = listing.get("price")

    if isinstance(price, dict):
        return price.get("value")

    return price


def explain_choice(listing, plan) -> str:

    reasons = []

    price = _get_price(listing)

    if price is None:
        return "missing price signal"

    if plan["max_price"] and price <= plan["max_price"]:
        reasons.append("fits budget")

    if plan["location"] and plan["location"] in str(listing.get("location", "")):
        reasons.append("good location match")

    if plan["internet_required"]:
        if "wifi" in str(listing.get("title", "")).lower():
            reasons.append("has internet")

    if not reasons:
        return "neutral option"

    return ", ".join(reasons)

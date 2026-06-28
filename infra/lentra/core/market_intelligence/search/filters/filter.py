def apply_filters(listings, parsed_query: dict):
    """
    MVP filter layer:
    - no DB calls
    - only in-memory filtering
    """

    if not listings:
        return []

    result = listings

    budget = parsed_query.get("budget")

    if budget:
        try:
            max_price = float(str(budget).replace("$", ""))
            result = [
                x for x in result
                if getattr(x, "price", 0) <= max_price
            ]
        except Exception:
            pass

    return result

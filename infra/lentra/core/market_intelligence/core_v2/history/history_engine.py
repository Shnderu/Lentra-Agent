

PRICE_HISTORY = {}


def record_price(city: str, cluster_id: str, price: float):

    key = f"{city}:{cluster_id}"

    if key not in PRICE_HISTORY:
        PRICE_HISTORY[key] = []

    PRICE_HISTORY[key].append(price)

    return PRICE_HISTORY[key]


def get_trend(city: str, cluster_id: str):

    key = f"{city}:{cluster_id}"

    history = PRICE_HISTORY.get(key, [])

    if len(history) < 2:
        return "stable"

    if history[-1] > history[0]:
        return "up"
    elif history[-1] < history[0]:
        return "down"

    return "stable"



from datetime import datetime

PRICE_HISTORY = {}


def record_price(cluster_id, price):

    if cluster_id not in PRICE_HISTORY:
        PRICE_HISTORY[cluster_id] = []

    PRICE_HISTORY[cluster_id].append({
        "ts": datetime.utcnow().isoformat(),
        "price": float(price)
    })

    return PRICE_HISTORY[cluster_id]


def get_price_trend(cluster_id):

    history = PRICE_HISTORY.get(cluster_id, [])

    if len(history) < 2:
        return "insufficient_data"

    prices = [h["price"] for h in history]

    first = prices[0]
    last = prices[-1]

    delta = (last - first) / first if first else 0

    if delta > 0.1:
        return "rising"
    elif delta < -0.1:
        return "dropping"
    else:
        return "stable"


def get_latest_price(cluster_id):

    history = PRICE_HISTORY.get(cluster_id, [])

    if not history:
        return None

    return history[-1]["price"]

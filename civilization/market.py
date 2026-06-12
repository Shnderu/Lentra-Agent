import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

BIDS = "stream:market:bids"


def select_winner(task_id):
    bids = r.xrange(BIDS)

    best = None
    best_price = float("inf")

    for _, b in bids:
        if b.get("task_id") == task_id:
            price = float(b.get("price", 9999))
            if price < best_price:
                best_price = price
                best = b

    return best

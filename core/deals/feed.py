
from core.deals.engine import DealEngine


engine = DealEngine()


def build_feed(origin=None):

    deals = engine.get_deals(origin)

    feed = []

    for d in deals:

        feed.append({
            "title": f"{d['origin']} → {d['destination']}",
            "price": d["price"],
            "badge": d["badge"],
            "score": d["score"],
            "cta": ["Buy", "Watch", "Share"]
        })

    return feed

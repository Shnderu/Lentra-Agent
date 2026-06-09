
from core.search.engine import SearchEngine
from core.deals.scorer import score_deal
from core.deals.filters import is_valid_deal


search_engine = SearchEngine()


class DealEngine:

    def get_deals(self, origin: str = None, limit: int = 10):

        raw = search_engine.search_route(
            origin=origin or "ANY",
            destination="ANY"
        )

        deals = []

        for r in raw["routes"]:

            if not is_valid_deal(r):
                continue

            deals.append({
                "origin": r["origin"],
                "destination": r["destination"],
                "price": r["price"],
                "airline": r["airline"],
                "score": score_deal(r["price"]),
                "badge": self._badge(r["price"])
            })

        deals.sort(key=lambda x: x["score"], reverse=True)

        return deals[:limit]

    def _badge(self, price):

        if price < 100:
            return "🔥 ERROR FARE"

        if price < 200:
            return "💸 DEAL"

        return "✈️ NORMAL"

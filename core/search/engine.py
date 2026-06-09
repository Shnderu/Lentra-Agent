from core.search.providers.base import search_routes
from core.search.scoring import score_deal


class SearchEngine:

    def search_route(self, origin: str, destination: str, date: str = None):

        raw_results = search_routes(origin, destination, date)

        normalized = []

        for r in raw_results:
            normalized.append({
                "origin": origin,
                "destination": destination,
                "price": r["price"],
                "currency": r.get("currency", "EUR"),
                "airline": r.get("airline", "unknown"),
                "departure": r.get("departure"),
                "arrival": r.get("arrival"),
                "score": score_deal(r["price"])
            })

        normalized.sort(key=lambda x: x["price"])

        return {
            "count": len(normalized),
            "best_price": normalized[0]["price"] if normalized else None,
            "routes": normalized
        }

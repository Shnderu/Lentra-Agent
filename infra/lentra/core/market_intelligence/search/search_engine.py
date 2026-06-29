class MarketSearchEngine:
    """
    Filters UI cards using structured query.
    """

    def search(self, cards: list, query: dict):

        results = cards

        # PRICE FILTER
        if query.get("min_price") is not None:
            results = [c for c in results if (c.get("price") or 0) >= query["min_price"]]

        if query.get("max_price") is not None:
            results = [c for c in results if (c.get("price") or 0) <= query["max_price"]]

        # LOCATION FILTER
        if query.get("location"):
            loc = query["location"]
            results = [
                c for c in results
                if loc in str(c.get("location", {})).lower()
                or loc in str(c.get("segment", "")).lower()
                or loc in str(c.get("micro_market", "")).lower()
            ]

        # RISK FILTER
        if query.get("max_risk") is not None:
            results = [
                c for c in results
                if (c.get("risk") or 0.5) <= query["max_risk"]
            ]

        return results

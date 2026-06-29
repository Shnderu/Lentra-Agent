class RankingEngine:

    def score(self, listing: dict, context: dict = None) -> float:

        price = float(listing.get("price") or 0)
        risk = float(listing.get("risk") or 0.5)
        area = float(listing.get("area_quality") or 5)

        # PURE SIGNAL ONLY (no business logic coupling)
        return (area / 10) * 0.5 + (1 - risk) * 0.5

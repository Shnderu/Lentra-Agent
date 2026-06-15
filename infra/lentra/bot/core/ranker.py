class AIRanker:

    def score(self, item: dict, filters: dict) -> float:

        score = item.get("score", 0)

        if filters.get("pool") and item.get("pool"):
            score += 0.5

        if filters.get("sea_view") and item.get("sea_view"):
            score += 0.7

        max_price = filters.get("max_price")
        if max_price and item.get("price_vnd_mln", 0) <= max_price:
            score += 0.3

        return round(score, 3)

    def rank(self, items: list, filters: dict):

        for i in items:
            i["ai_score"] = self.score(i, filters)

        return sorted(items, key=lambda x: x["ai_score"], reverse=True)

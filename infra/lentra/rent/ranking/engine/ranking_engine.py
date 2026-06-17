from lentra.rent.learning.weights.weight_store import WeightStore


class RankingEngine:

    def __init__(self):
        self.store = WeightStore()

    def score(self, item: dict, query: dict) -> float:
        w = self.store.get()

        score = 0.0

        if item.get("price"):
            score += w["price"]

        if item.get("location"):
            score += w["location"]

        if item.get("title"):
            score += w["title"]

        text = query.get("text", "").lower()
        title = (item.get("title") or "").lower()

        if text and title and text in title:
            score += w["text_match"]

        if item.get("source") == "default_connector":
            score += w["source"]

        item["score"] = score
        return item

    def rank(self, items: list, query: dict) -> list:
        scored = [self.score(i, query) for i in items]
        return sorted(scored, key=lambda x: x["score"], reverse=True)

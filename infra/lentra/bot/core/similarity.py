class SimilarityEngine:

    def score(self, a: dict, b: dict) -> float:

        score = 0

        if a.get("city") == b.get("city"):
            score += 0.4

        if a.get("district") == b.get("district"):
            score += 0.3

        if a.get("pool") == b.get("pool"):
            score += 0.1

        if a.get("sea_view") == b.get("sea_view"):
            score += 0.1

        price_diff = abs(a.get("price_vnd_mln", 0) - b.get("price_vnd_mln", 0))
        score += max(0, 0.2 - price_diff * 0.02)

        return round(score, 3)

    def find_similar(self, item: dict, items: list):

        return sorted(
            items,
            key=lambda x: self.score(item, x),
            reverse=True
        )[:5]

from lentra.bot.state.profile_store import ProfileStore


class RecommendationEngine:

    def __init__(self):
        self.store = ProfileStore()

    def recommend(self, user_id: int, items: list):

        profile = self.store.load(user_id)

        scored = []

        for item in items:

            score = 0

            if item.get("city") in profile.preferred_cities:
                score += 0.4

            if item.get("id") in profile.clicked_items:
                score += 0.3

            if item.get("pool"):
                score += profile.feature_weights["pool"]

            if item.get("sea_view"):
                score += profile.feature_weights["sea_view"]

            score += (10 - item.get("price_vnd_mln", 10)) * 0.05

            item["rec_score"] = round(score, 3)
            scored.append(item)

        return sorted(scored, key=lambda x: x["rec_score"], reverse=True)

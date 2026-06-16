from lentra.bot.state.profile import UserProfile


class PersonalizationEngine:

    def score(self, item: dict, profile: UserProfile) -> float:

        score = item.get("score", 0)

        # CITY BIAS
        if item.get("city") in profile.preferred_cities:
            score += 0.3

        # CLICK HISTORY BIAS
        if item["id"] in profile.clicked_items:
            score += 0.5

        # SAVE HISTORY BIAS
        if item["id"] in profile.saved_items:
            score += 0.7

        # PRICE PREFERENCE LEARNING (simple heuristic)
        if profile.preference_bias.get("cheap") and item.get("price_vnd_mln", 0) < 10:
            score += 0.2

        return score

    def rank(self, items: list, profile: UserProfile):

        for item in items:
            item["personal_score"] = self.score(item, profile)

        return sorted(items, key=lambda x: x["personal_score"], reverse=True)

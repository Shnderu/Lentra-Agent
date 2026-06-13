# ============================================================
# UX VALUE ENGINE V17.4
# ============================================================

class UXEngine:

    def format_response(self, ranked_list):
        if not ranked_list:
            return {
                "message": "no results found"
            }

        best = ranked_list[0]
        others = ranked_list[1:3]

        return {
            "best_choice": best,
            "alternatives": others,
            "why_this_is_best": self._explain(best),
            "confidence": best.get("score", 0.5)
        }

    def _explain(self, item):
        reasons = []

        if item.get("price_score", 0) < 0:
            reasons.append("below market price")

        if item.get("trust_score", 0) > 70:
            reasons.append("high trust source")

        if item.get("geo_score", 0) > 70:
            reasons.append("optimal location")

        return reasons

# ============================================================
# RANKER V1 (MVP CORE VALUE ENGINE)
# ============================================================

class Ranker:

    def rank(self, listings, request):
        budget = request.get("budget", 10000)

        scored = []

        for l in listings:
            score = 0

            # price factor (cheaper = better)
            if l["price"] <= budget:
                score += 40
            else:
                score -= 20

            # location factor
            score += l.get("location_score", 0) * 0.3

            # trust factor
            score += l.get("trust_score", 0) * 0.4

            l["score"] = score
            scored.append(l)

        return sorted(scored, key=lambda x: x["score"], reverse=True)

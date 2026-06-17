from typing import List


class AdvancedRanker:

    def rank(self, listings: List, session: dict):

        city_pref = session.get("city")
        budget_pref = session.get("budget")

        scored = []

        for l in listings:

            score = 0

            # -------------------------
            # 1. GEO SCORE
            # -------------------------
            if city_pref and l.city:
                if l.city.lower() == city_pref.lower():
                    score += 60
                else:
                    score -= 10

            # -------------------------
            # 2. BUDGET FIT
            # -------------------------
            if budget_pref and l.price:
                diff = budget_pref - l.price

                if diff >= 0:
                    score += 40
                    score += min(diff / budget_pref * 20, 20)
                else:
                    score -= 30

            # -------------------------
            # 3. PRICE NORMALIZATION
            # -------------------------
            if l.price:
                # дешевые варианты получают небольшой бонус
                score += max(0, 1000 - l.price) / 200

            # -------------------------
            # 4. SOURCE QUALITY
            # -------------------------
            if getattr(l, "source", None) == "real_api":
                score += 10

            if getattr(l, "source", None) == "mock":
                score += 0

            # -------------------------
            # 5. AVAILABILITY / VALIDITY
            # -------------------------
            if hasattr(l, "available") and not l.available:
                score -= 100

            # -------------------------
            # 6. FRESHNESS (optional)
            # -------------------------
            if hasattr(l, "timestamp") and l.timestamp:
                age = 2026 - l.timestamp.year
                score -= age * 5

            scored.append((score, l))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [l for _, l in scored]

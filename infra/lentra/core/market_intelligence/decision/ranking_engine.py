
class RankingEngine:

    def run(self, objects, persona=None):

        ranked = []

        for obj in objects:

            score = 0.0

            price = getattr(obj, "market_price", 0) or 0
            risk = getattr(obj, "risk", 0.5)
            area = getattr(obj, "area_score", 5)
            conf = getattr(obj, "confidence", 0.5)

            if price > 0:
                score += max(0, 1 - price / 1000) * 0.3

            score += (1 - risk) * 0.3
            score += (area / 10) * 0.2
            score += conf * 0.2

            # 🔥 SAFE ATTACH (НЕ ЛОМАЕТ МОДЕЛЬ)
            setattr(obj, "final_score", round(score, 3))

            ranked.append(obj)

        ranked.sort(key=lambda x: getattr(x, "final_score", 0), reverse=True)

        return ranked


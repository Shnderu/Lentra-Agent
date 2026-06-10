from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.ranking.engine import FlightRankingEngine


class FlightExplanationEngine:

    def __init__(self):
        self.ranker = FlightRankingEngine()

    def explain(self, offers: list[FlightOffer]) -> dict:

        if not offers:
            return {
                "summary": "❌ Рейсы не найдены",
                "best": None,
                "reasons": []
            }

        ranked = self.ranker.rank(offers)

        best = ranked[0]
        score_best = self.ranker.score(best)

        reasons = self._build_reasons(best)

        return {
            "summary": "✈️ Найдены оптимальные варианты перелёта",
            "best": best,
            "best_score": round(score_best, 3),
            "reasons": reasons,
            "count": len(offers)
        }

    def _build_reasons(self, offer: FlightOffer) -> list[str]:

        reasons = []

        # цена
        if offer.price <= 150:
            reasons.append("Низкая цена относительно рынка")
        elif offer.price <= 300:
            reasons.append("Средний ценовой диапазон")
        else:
            reasons.append("Высокая цена, но компенсируется другими факторами")

        # длительность
        if "h" in offer.duration:
            try:
                hours = int(offer.duration.split("h")[0])
                if hours <= 3:
                    reasons.append("Короткий перелёт")
                elif hours <= 6:
                    reasons.append("Средняя длительность рейса")
                else:
                    reasons.append("Длительный перелёт")
            except:
                pass

        # провайдер
        if offer.provider in ["amadeus", "kiwi"]:
            reasons.append("Данные из авиационного источника")
        elif offer.provider == "mock":
            reasons.append("Демо-данные (требуется API интеграция)")

        return reasons

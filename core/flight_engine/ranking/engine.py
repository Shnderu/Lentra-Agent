from typing import List
from core.flight_engine.gateway.dto import FlightOffer
from core.llm.router import GridLLMRouter


class FlightRankingEngine:

    def __init__(self):
        self.llm = GridLLMRouter()

        # базовые веса (детерминированный слой)
        self.weights = {
            "price": 0.5,
            "duration": 0.2,
            "provider": 0.1,
            "llm_score": 0.2
        }

    def _normalize_price(self, offers: List[FlightOffer]):
        prices = [o.price for o in offers if o.price]
        if not prices:
            return {}

        min_p, max_p = min(prices), max(prices)

        return {
            o: (1 - (o.price - min_p) / (max_p - min_p + 1e-6))
            for o in offers
        }

    def _duration_to_score(self, offer: FlightOffer):
        try:
            # грубая нормализация (2h30m → 150 min)
            text = offer.duration.lower().replace("h", " ").replace("m", "")
            parts = text.split()
            hours = int(parts[0]) if len(parts) > 0 else 0
            mins = int(parts[1]) if len(parts) > 1 else 0
            total = hours * 60 + mins

            # чем меньше — тем лучше
            return max(0, 1 - total / 1000)
        except:
            return 0.5

    def _provider_score(self, offer: FlightOffer):
        # trust map (можно расширять)
        trust = {
            "kiwi": 0.9,
            "amadeus": 0.95,
            "mock": 0.2
        }
        return trust.get(offer.provider, 0.5)

    async def _llm_score(self, offer: FlightOffer):

        prompt = [
            {
                "role": "system",
                "content": (
                    "You evaluate flight quality. "
                    "Return ONLY number 0-1 (float)."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Flight:\n"
                    f"price={offer.price} {offer.currency}\n"
                    f"duration={offer.duration}\n"
                    f"airline={offer.airline}\n"
                    f"provider={offer.provider}"
                )
            }
        ]

        result = await self.llm.reason(str(prompt))

        try:
            return float(result.strip())
        except:
            return 0.5

    async def rank(self, offers: List[FlightOffer]) -> List[FlightOffer]:

        if not offers:
            return []

        price_map = self._normalize_price(offers)

        scored = []

        for o in offers:

            price_score = price_map.get(o, 0.5)
            duration_score = self._duration_to_score(o)
            provider_score = self._provider_score(o)

            llm_score = await self._llm_score(o)

            final_score = (
                price_score * self.weights["price"] +
                duration_score * self.weights["duration"] +
                provider_score * self.weights["provider"] +
                llm_score * self.weights["llm_score"]
            )

            scored.append((final_score, o))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [o for _, o in scored]

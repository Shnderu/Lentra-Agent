from core.flight_engine.gateway.dto import FlightOffer
import re


class AIRankingEngineV2:

    def __init__(self, intent: str = "balanced"):
        self.intent = intent

        # базовые веса
        self.weights = self._set_weights(intent)

    def _set_weights(self, intent: str):

        if intent == "budget":
            return {"price": 0.7, "duration": 0.2, "provider": 0.1}

        if intent == "fast":
            return {"price": 0.2, "duration": 0.7, "provider": 0.1}

        # balanced default
        return {"price": 0.5, "duration": 0.3, "provider": 0.2}

    def _extract_minutes(self, duration: str) -> int:
        try:
            match = re.search(r"(\d+)h", duration)
            hours = int(match.group(1)) if match else 0

            match_m = re.search(r"(\d+)m", duration)
            minutes = int(match_m.group(1)) if match_m else 0

            return hours * 60 + minutes
        except:
            return 999

    def _normalize_price(self, price: float, prices: list[float]) -> float:
        if not prices:
            return 0

        min_p = min(prices)
        max_p = max(prices)

        if max_p == min_p:
            return 1.0

        # чем дешевле — тем ближе к 1
        return 1 - ((price - min_p) / (max_p - min_p))

    def _provider_score(self, provider: str) -> float:

        scores = {
            "amadeus": 1.0,
            "kiwi": 0.9,
            "mock": 0.3,
            "affiliate": 0.6
        }

        return scores.get(provider, 0.5)

    def score(self, offer: FlightOffer, all_offers: list[FlightOffer]) -> float:

        prices = [o.price for o in all_offers]
        price_score = self._normalize_price(offer.price, prices)

        duration_score = 1 - (self._extract_minutes(offer.duration) / 1000)
        duration_score = max(0, min(duration_score, 1))

        provider_score = self._provider_score(offer.provider)

        w = self.weights

        return (
            price_score * w["price"] +
            duration_score * w["duration"] +
            provider_score * w["provider"]
        )

    def rank(self, offers: list[FlightOffer]) -> list[FlightOffer]:

        scored = [
            (o, self.score(o, offers))
            for o in offers
        ]

        scored.sort(key=lambda x: x[1], reverse=True)

        return [o for o, _ in scored]

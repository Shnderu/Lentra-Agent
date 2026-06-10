from typing import List
from core.flight_engine.gateway.dto import FlightOffer
from core.llm.router import GridLLMRouter


class FlightRankingEngineV2:

    def __init__(self):
        self.llm = GridLLMRouter()

    async def _evaluate(self, offer: FlightOffer):

        prompt = [
            {
                "role": "system",
                "content": (
                    "You are a flight ranking AI.\n"
                    "Return ONLY JSON:\n"
                    "{"
                    "\"score\": float (0-1),"
                    "\"reason\": string,"
                    "\"risk\": string (low/medium/high)"
                    "}"
                )
            },
            {
                "role": "user",
                "content": (
                    f"origin: {offer.origin}\n"
                    f"destination: {offer.destination}\n"
                    f"price: {offer.price} {offer.currency}\n"
                    f"duration: {offer.duration}\n"
                    f"airline: {offer.airline}\n"
                    f"provider: {offer.provider}"
                )
            }
        ]

        result = await self.llm.reason(str(prompt))

        try:
            import json
            return json.loads(result)
        except:
            return {
                "score": 0.5,
                "reason": "fallback parsing error",
                "risk": "medium"
            }

    async def rank(self, offers: List[FlightOffer]):

        scored = []

        for offer in offers:

            evaluation = await self._evaluate(offer)

            scored.append({
                "offer": offer,
                "score": evaluation["score"],
                "reason": evaluation["reason"],
                "risk": evaluation["risk"]
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored

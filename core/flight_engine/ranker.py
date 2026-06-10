from typing import List
from core.flight_engine.gateway.dto import FlightOffer


class FlightRanker:

    def rank(self, offers: List[FlightOffer]) -> List[FlightOffer]:

        if not offers:
            return []

        # -------------------------
        # 1. REMOVE DUPLICATES
        # -------------------------
        unique = {}
        for o in offers:
            key = (o.origin, o.destination, o.price, o.duration)

            # keep cheapest duplicate
            if key not in unique or o.price < unique[key].price:
                unique[key] = o

        offers = list(unique.values())

        # -------------------------
        # 2. SCORING MODEL
        # -------------------------
        def score(o: FlightOffer):

            price_score = 1 / (o.price + 1)

            duration_score = 0
            if o.duration:
                try:
                    # naive parsing "2h 10m"
                    hours = 0
                    minutes = 0

                    if "h" in o.duration:
                        parts = o.duration.split("h")
                        hours = int(parts[0])

                        if "m" in parts[1]:
                            minutes = int(parts[1].replace("m", "").strip())

                    duration_score = 1 / (hours * 60 + minutes + 1)

                except:
                    duration_score = 0

            provider_bonus = 0.1 if o.provider == "amadeus" else 0.05

            return price_score + duration_score + provider_bonus

        # attach score
        for o in offers:
            o._score = score(o)

        # -------------------------
        # 3. SORT
        # -------------------------
        offers.sort(key=lambda x: x._score, reverse=True)

        return offers

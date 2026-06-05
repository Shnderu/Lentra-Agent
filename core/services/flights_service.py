import logging


class FlightsService:
    def search(self, from_city: str, to_city: str, date: str):
        logging.info(f"SEARCH FLIGHTS {from_city} -> {to_city} | {date}")

        return [
            {
                "airline": "FlyRum Demo",
                "price": 14900,
                "currency": "RUB",
                "from": from_city,
                "to": to_city,
                "date": date
            }
        ]


flights_service = FlightsService()

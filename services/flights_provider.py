import random

class FlightsProvider:
    def search(self, route: str):
        return {
            "route": route,
            "price": random.randint(120, 600),
            "currency": "EUR"
        }

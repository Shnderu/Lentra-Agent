import random


class FlightProvider:

    def search(self, from_code: str, to_code: str, date: str):
        """
        MOCK LAYER (готово под Kiwi / Amadeus)
        """

        results = []

        for i in range(5):
            results.append({
                "airline": random.choice(["FlyDubai", "Pegasus", "Aegean", "Turkish Airlines"]),
                "price": random.randint(80, 450),
                "from": from_code,
                "to": to_code,
                "date": date,
                "duration": random.randint(2, 12)
            })

        return results


flight_provider = FlightProvider()

import random


def search_routes(origin, destination, date=None):

    # STUB PROVIDER (позже заменишь на API / scraping / aggregators)

    results = []

    for i in range(5):

        results.append({
            "price": random.randint(50, 500),
            "currency": "EUR",
            "airline": random.choice(["Lufthansa", "WizzAir", "AirFrance"]),
            "departure": "10:00",
            "arrival": "14:00"
        })

    return results

def handle_rent_search(task):
    city = task.payload.get("city")

    # MOCK provider layer (позже заменим на реальные источники)
    return [
        {
            "title": f"Apartment in {city}",
            "price": 850,
            "currency": "USD",
            "city": city,
            "source": "mock"
        }
    ]

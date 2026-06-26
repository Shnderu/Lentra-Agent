
def fetch_listings(query):
    # MVP stub (позже заменишь на FB/Telegram/сайты)
    return [
        {
            "id": "1",
            "title": "Studio near beach",
            "price": 700,
            "currency": "USD",
            "location": query["city"],
            "source": "mock"
        },
        {
            "id": "2",
            "title": "Modern apartment center",
            "price": 650,
            "currency": "USD",
            "location": query["city"],
            "source": "mock"
        }
    ]

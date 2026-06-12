import json


def handle_rent_search(task: dict):
    """
    Deterministic business logic layer (mock provider stage).
    """

    payload = task.get("payload", {})
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}

    city = payload.get("city", "unknown")

    # MOCK provider response
    results = [
        {
            "title": f"Apartment in {city}",
            "price": 850,
            "currency": "USD",
            "source": "faswaz"
        }
    ]

    return {
        "ok": True,
        "result": {
            "city": city,
            "items": results
        }
    }

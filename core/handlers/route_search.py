import random


def process(task):
    payload = task.get("payload", {})

    origin = payload.get("origin", "UNKNOWN")
    destination = payload.get("destination", "UNKNOWN")

    result = {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "airline": "FlyRum Demo Air",
        "price": random.randint(35000, 65000),
    }

    print("[ROUTE RESULT]", result)

    return result

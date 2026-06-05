from events.bus import publish

def process_flight_event(event: dict):
    price = event.get("price", 0)

    if price < 100:
        publish({
            "type": "alert",
            "level": "HIGH",
            "message": f"Cheap flight detected: {price}",
            "data": event
        })
    elif price < 300:
        publish({
            "type": "alert",
            "level": "MEDIUM",
            "message": f"Good deal: {price}",
            "data": event
        })

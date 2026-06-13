from lentra.events.stream import publish


def track_feedback(user_id: int, property_id: int, event: str):
    publish("feedback", {
        "user_id": user_id,
        "property_id": property_id,
        "event": event
    })

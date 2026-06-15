from datetime import datetime


def build_event(user_id: int, property_id: int, event_type: str, meta=None):
    return {
        "user_id": user_id,
        "property_id": property_id,
        "event_type": event_type,  # view | click | like
        "meta": meta or {},
        "timestamp": datetime.utcnow().isoformat()
    }

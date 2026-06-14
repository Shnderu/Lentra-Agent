def detect_intent(payload: dict):
    """
    Simple deterministic intent router v1
    """

    text = (payload.get("text") or "").lower()

    if "rent" in text or "apartment" in text:
        return "search_property"

    if "ranking" in text:
        return "ranking_event"

    return "parse_property"


def build_context(payload: dict):
    """
    Minimal state container
    """

    return {
        "city": payload.get("city"),
        "budget": payload.get("budget", 1000),
        "raw": payload
    }

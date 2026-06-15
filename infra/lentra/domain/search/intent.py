def detect_intent(text: str):
    if not text:
        return {}

    t = text.lower()

    intent = {
        "cheap": 0.0,
        "luxury": 0.0,
        "beach": 0.0
    }

    if any(w in t for w in ["cheap", "budget", "low price", "under"]):
        intent["cheap"] = 1.0

    if any(w in t for w in ["luxury", "premium", "expensive", "modern studio"]):
        intent["luxury"] = 1.0

    if any(w in t for w in ["beach", "sea", "ocean", "sea view"]):
        intent["beach"] = 1.0

    return intent

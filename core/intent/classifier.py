class Intent:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence


def classify(text: str, source="message"):

    text = (text or "").lower()

    print("🔥 CLASSIFY INPUT:", text)

    if "самара" in text:
        return Intent("route_search", 0.99)

    return Intent("unknown", 0.1)

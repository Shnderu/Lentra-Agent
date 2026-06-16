class IntentClassifier:
    """
    Minimal production classifier (rule-based baseline).
    """

    def classify(self, text: str) -> str:
        text = (text or "").lower().strip()

        if not text:
            return "fallback"

        route_keywords = ["flight", "route", "from", "to", "ticket"]

        if any(k in text for k in route_keywords):
            return "route_search"

        return "search"

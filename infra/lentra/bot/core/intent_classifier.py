class IntentClassifier:
    """
    Minimal production classifier (rule-based baseline).
    """

    def classify(self, text: str) -> str:
        text = (text or "").lower().strip()

        if not text:
            return "fallback"

        # very simple routing logic (MVP)
        return "search"

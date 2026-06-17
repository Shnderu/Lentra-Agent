class IntentClassifier:
    def classify(self, text: str) -> str:
        if "rent" in text:
            return "rent_search"
        return "fallback"

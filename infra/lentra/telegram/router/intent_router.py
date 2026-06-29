class IntentRouter:

    def detect(self, text: str) -> str:

        text = (text or "").lower()

        if "compare" in text:
            return "compare"

        if "why" in text or "explain" in text:
            return "explain"

        if "alert" in text or "notify" in text:
            return "alert"

        if "area" in text or "district" in text:
            return "area"

        return "search"

class TelegramUpdateAdapter:
    def __init__(self, trace=None):
        self.trace = trace

    def normalize(self, tg_update: dict) -> dict:

        if self.trace:
            self.trace.node("telegram_update_received", tg_update)

        message = tg_update.get("message", {})
        text = message.get("text", "")

        intent = self._detect_intent(text)

        if self.trace:
            self.trace.node("intent_detected", {"intent": intent})

        return {
            "update_id": tg_update.get("update_id"),
            "intent": intent,
            "payload": {
                "text": text,
                "user_id": message.get("from", {}).get("id"),
            }
        }

    def _detect_intent(self, text: str) -> str:
        if "rent" in text.lower():
            return "rent_search"
        return "unknown"

from enum import Enum

class IntentType(str, Enum):
    GENERIC = "generic"
    INFO = "info"
    ACTION = "action"
    ALERT = "alert"

class Router:
    def classify(self, text: str) -> IntentType:
        # временно rule-based, позже LLM
        text = text.lower()

        if "напомни" in text or "alert" in text:
            return IntentType.ALERT

        if "как" in text or "что" in text:
            return IntentType.INFO

        if "забронировать" in text or "создать" in text:
            return IntentType.ACTION

        return IntentType.GENERIC

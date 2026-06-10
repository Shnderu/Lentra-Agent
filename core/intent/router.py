from core.intent.llm_classifier import LLMIntentClassifier


class IntentRouter:

    def __init__(self):
        self.llm = LLMIntentClassifier()

    async def route(self, text):

        # HARD NORMALIZATION (убивает все edge cases)
        if hasattr(text, "text"):
            text = text.text

        if hasattr(text, "caption"):
            text = text.caption

        if text is None:
            text = ""

        text = str(text)

        result = await self.llm.classify(text)

        intent = result.get("intent", "unknown")
        confidence = result.get("confidence", 0.0)

        text_lower = text.lower()

        if confidence < 0.6:
            if "flight" in text_lower or "рейс" in text_lower:
                intent = "route_search"
            else:
                intent = "unknown"

        return {
            "intent": intent,
            "confidence": confidence
        }


# backward compat (НОРМАЛЬНЫЙ SAFE WRAPPER)
async def route(text):
    return await IntentRouter().route(text)

from core.intent.router import IntentRouter
import logging

class UnifiedRuntime:

    def __init__(self):
        self.router = IntentRouter()

    async def unified_entry(self, message, context=None):

        try:
            text = message.text or message.caption or ""

            if not text:
                return {
                    "intent": "empty",
                    "confidence": 0.0
                }

            return await self.router.route(text)

        except Exception as e:
            logging.exception("UNIFIED_RUNTIME_ERROR")
            return {
                "intent": "error",
                "confidence": 0.0,
                "error": str(e)
            }


async def unified_entry(message, context=None):
    runtime = UnifiedRuntime()
    return await runtime.unified_entry(message, context)

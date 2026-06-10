import json
from core.llm.router import GridLLMRouter


class LLMIntentClassifier:

    def __init__(self):
        self.llm = GridLLMRouter()

    async def classify(self, text: str):

        result = await self.llm.intent(text)

        if not result:
            return {"intent": "unknown", "confidence": 0.0}

        try:
            return json.loads(result)
        except Exception:
            return {"intent": "unknown", "confidence": 0.0}

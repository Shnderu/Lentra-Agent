import os
from core.llm.grid_client import GridClient


class GridLLMRouter:

    def __init__(self):
        self.client = GridClient()

        self.intent_model = os.getenv("LLM_MODEL_INTENT", "gpt-5.4-mini")
        self.reasoning_model = os.getenv("LLM_MODEL_REASONING", "claude-sonnet-4-6")
        self.fallback_model = os.getenv("LLM_MODEL_FALLBACK", "claude-haiku-4-5-20251001")

    async def call(self, messages, mode: str = "intent"):

        if mode == "intent":
            model = self.intent_model
        elif mode == "reasoning":
            model = self.reasoning_model
        else:
            model = self.fallback_model

        # 1. primary call
        result = await self.client.chat(model, messages)

        if result:
            return result

        # 2. fallback
        return await self.client.chat(self.fallback_model, messages)

    async def intent(self, text: str):

        messages = [
            {
                "role": "system",
                "content": (
                    "You are intent classifier. "
                    "Return ONLY JSON: {intent, confidence}"
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]

        return await self.call(messages, mode="intent")

    async def reason(self, text: str):

        messages = [
            {
                "role": "system",
                "content": "You are travel assistant reasoning engine."
            },
            {
                "role": "user",
                "content": text
            }
        ]

        return await self.call(messages, mode="reasoning")

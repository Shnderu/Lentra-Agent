import os
import httpx


class LLMClient:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    async def chat(self, messages, temperature: float = 0.2):

        if not self.api_key:
            return None

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature
                }
            )

            data = resp.json()

            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                return None

import os
import httpx


class GridClient:

    def __init__(self):
        self.api_key = os.getenv("GRID_API_KEY")
        self.base_url = os.getenv("GRID_BASE_URL")

    async def chat(self, model: str, messages, temperature: float = 0.2):

        if not self.api_key:
            return None

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )

                data = resp.json()
                return data["choices"][0]["message"]["content"]

            except Exception as e:
                print("[GRID CLIENT ERROR]", e)
                return None

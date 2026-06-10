import os
import json
import httpx


class LLMIntentClassifier:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")  # можно заменить позже
        self.enabled = bool(self.api_key)

    async def classify(self, origin: str, destination: str, date: str = None) -> dict:

        # -----------------------------
        # fallback без LLM
        # -----------------------------
        if not self.enabled:
            return {
                "intent": "balanced",
                "confidence": 0.5,
                "source": "fallback"
            }

        prompt = f"""
Ты классифицируешь намерение пользователя для поиска авиабилетов.

Данные:
origin: {origin}
destination: {destination}
date: {date}

Верни JSON строго в формате:
{{
  "intent": "budget|fast|business|balanced",
  "confidence": 0.0-1.0,
  "reason": "short explanation"
}}

Правила:
- budget = дешёвый билет важнее всего
- fast = минимальное время перелёта
- business = комфорт / premium / бизнес класс
- balanced = баланс цены и времени
"""

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.2
                    }
                )

            data = resp.json()

            content = data["choices"][0]["message"]["content"]

            try:
                parsed = json.loads(content)
            except:
                parsed = {
                    "intent": "balanced",
                    "confidence": 0.5,
                    "source": "parse_fallback"
                }

            parsed["source"] = "llm"
            return parsed

        except Exception as e:
            return {
                "intent": "balanced",
                "confidence": 0.5,
                "source": "error_fallback",
                "error": str(e)
            }

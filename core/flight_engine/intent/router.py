import re


class IntentRouter:

    def detect(self, origin: str, destination: str, date: str = None) -> dict:

        text = f"{origin} {destination}".lower()

        intent = "balanced"
        confidence = 0.6
        flags = []

        # --------------------------
        # 1. Budget intent
        # --------------------------
        if any(word in text for word in ["cheap", "low", "дешев", "бюджет"]):
            intent = "budget"
            confidence = 0.85
            flags.append("keyword_budget")

        # --------------------------
        # 2. Fast intent
        # --------------------------
        if any(word in text for word in ["fast", "quick", "быстр", "срочно"]):
            intent = "fast"
            confidence = 0.85
            flags.append("keyword_fast")

        # --------------------------
        # 3. Business / comfort (эвристика)
        # --------------------------
        if any(word in text for word in ["business", "premium", "comfort", "бизнес"]):
            intent = "business"
            confidence = 0.9
            flags.append("keyword_business")

        # --------------------------
        # 4. Short route heuristic
        # --------------------------
        if len(origin) == 3 and len(destination) == 3:
            flags.append("iata_detected")

        # --------------------------
        # 5. fallback logic
        # --------------------------
        if intent == "balanced" and date:
            # если дата есть → слегка смещаем к balanced premium
            confidence = 0.7

        return {
            "intent": intent,
            "confidence": confidence,
            "flags": flags
        }

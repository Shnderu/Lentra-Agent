import re


class RentIntelligenceEngine:
    """
    Восстановленный бизнес-слой:
    превращает сырой текст → структурированный intent
    """

    def parse(self, text: str) -> dict:
        text_l = text.lower()

        if "rent" not in text_l:
            return {
                "intent": "UNKNOWN",
                "confidence": 0.2
            }

        city = self._extract_city(text)
        budget = self._extract_budget(text)
        room_type = self._extract_type(text)

        confidence = 0.6
        if city:
            confidence += 0.2
        if budget:
            confidence += 0.1
        if room_type:
            confidence += 0.1

        return {
            "intent": "RENT",
            "city": city,
            "budget": budget,
            "type": room_type,
            "confidence": round(confidence, 2)
        }

    def _extract_city(self, text: str):
        cities = ["bangkok", "ho chi minh", "saigon", "bali", "phuket"]
        for c in cities:
            if c in text.lower():
                return c
        return None

    def _extract_budget(self, text: str):
        match = re.search(r"\$?(\d{3,5})", text)
        if match:
            return int(match.group(1))
        return None

    def _extract_type(self, text: str):
        if "studio" in text.lower():
            return "studio"
        if "apartment" in text.lower():
            return "apartment"
        if "villa" in text.lower():
            return "villa"
        return None

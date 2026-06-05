import re


class AIParser:
    def parse_flight_query(self, text: str) -> dict:
        text = text.lower()

        return {
            "from": self._extract_from(text),
            "to": self._extract_to(text),
            "date": self._extract_date(text)
        }

    def _extract_from(self, text: str):
        if "моск" in text:
            return "MOW"
        return None

    def _extract_to(self, text: str):
        if "стамбул" in text:
            return "IST"
        return None

    def _extract_date(self, text: str):
        match = re.search(r"(\d{1,2})\s?(июл|июня|авг|августа)", text)
        return match.group(0) if match else None


ai_parser = AIParser()

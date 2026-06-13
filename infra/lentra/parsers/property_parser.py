import re


class PropertyParser:
    """
    V2 semantic parser + confidence scoring (full model)
    """

    def parse(self, text: str) -> dict:
        if not text:
            return {}

        t = text.lower()

        price = self._extract_price(t)
        currency = self._extract_currency(t)
        location = self._extract_location(text)
        ptype = self._extract_type(t)

        confidence = self._calculate_confidence(
            text=t,
            price=price,
            currency=currency,
            location=location,
            ptype=ptype
        )

        return {
            "price": price,
            "currency": currency,
            "location": location,
            "type": ptype,
            "confidence": confidence,
            "raw_text": text
        }

    # ----------------------------
    # PRICE
    # ----------------------------
    def _extract_price(self, text: str):
        match = re.search(r'(\d{2,6})\s?\$|(\d{2,6})\s?usd', text)
        if match:
            return int(match.group(1) or match.group(2))
        return None

    # ----------------------------
    # CURRENCY
    # ----------------------------
    def _extract_currency(self, text: str):
        if "$" in text or "usd" in text:
            return "USD"
        if "vnd" in text:
            return "VND"
        return None

    # ----------------------------
    # LOCATION
    # ----------------------------
    def _extract_location(self, text: str):
        locations = [
            "danang",
            "da nang",
            "hanoi",
            "hcmc",
            "saigon"
        ]

        t = text.lower()
        for loc in locations:
            if loc in t:
                return loc

        return None

    # ----------------------------
    # TYPE
    # ----------------------------
    def _extract_type(self, text: str):
        if "studio" in text:
            return "studio"
        if "apartment" in text or "apt" in text:
            return "apartment"
        if "house" in text or "villa" in text:
            return "house"
        if "room" in text:
            return "room"

        return "unknown"

    # ----------------------------
    # CONFIDENCE MODEL
    # ----------------------------
    def _calculate_confidence(self, text, price, currency, location, ptype):
        score = 0.0

        if price:
            score += 0.3
        if currency:
            score += 0.1
        if location:
            score += 0.25
        if ptype and ptype != "unknown":
            score += 0.2

        if "$" in text:
            score += 0.05
        if "rent" in text or "for rent" in text:
            score += 0.1

        if len(text) > 80:
            score += 0.05

        return round(min(score, 1.0), 3)

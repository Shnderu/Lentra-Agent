import re

class QueryParser:
    """
    Converts natural language query into structured search filters.
    """

    def parse(self, text: str) -> dict:

        text = (text or "").lower()

        query = {
            "min_price": None,
            "max_price": None,
            "location": None,
            "max_risk": None
        }

        # -------------------------
        # PRICE PATTERN
        # -------------------------
        price_match = re.search(r"(\d{2,5})\s?\$", text)
        if price_match:
            query["max_price"] = int(price_match.group(1))

        under_match = re.search(r"under\s(\d{2,5})", text)
        if under_match:
            query["max_price"] = int(under_match.group(1))

        # -------------------------
        # LOCATION SIGNALS
        # -------------------------
        if "beach" in text:
            query["location"] = "beach"

        if "center" in text:
            query["location"] = "center"

        if "da nang" in text:
            query["location"] = "da_nang"

        if "bangkok" in text:
            query["location"] = "bangkok"

        if "bali" in text:
            query["location"] = "bali"

        # -------------------------
        # RISK INTENT
        # -------------------------
        if "safe" in text or "low risk" in text:
            query["max_risk"] = 0.5

        if "cheap" in text or "budget" in text:
            query["max_risk"] = 0.9

        return query

import re
from typing import Dict, Any


class RentalParser:
    """
    MVP parser для аренды жилья.

    Извлекает:
    - цену
    - тип жилья
    - город (очень упрощённо)
    """

    CITY_KEYWORDS = {
        "da nang": "da nang",
        "danang": "da nang",
        "bangkok": "bangkok",
        "bali": "bali",
        "chiang mai": "chiang mai"
    }

    TYPE_KEYWORDS = {
        "studio": "studio",
        "apartment": "apartment",
        "condo": "condo",
        "room": "room"
    }

    def parse(self, text: str) -> Dict[str, Any]:

        lower_text = text.lower()

        # price extraction
        price_match = re.search(r'(\d{2,5})\s*\$', lower_text)
        price = int(price_match.group(1)) if price_match else None

        # city detection
        city = None
        for k, v in self.CITY_KEYWORDS.items():
            if k in lower_text:
                city = v
                break

        # type detection
        rtype = None
        for k, v in self.TYPE_KEYWORDS.items():
            if k in lower_text:
                rtype = v
                break

        return {
            "raw": text,
            "price": price,
            "city": city,
            "type": rtype
        }

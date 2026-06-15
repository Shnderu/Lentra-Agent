import re
from typing import Dict, Any, Optional


def parse_query(text: Optional[str]) -> Dict[str, Any]:
    """
    QUERY DSL v1 parser
    Преобразует текст Telegram запроса в structured filters
    """

    if not text:
        return {}

    text = text.strip().lower()

    filters: Dict[str, Any] = {}

    # PRICE: "< 500", "under 500", "max 700"
    price_match = re.search(r"(?:<|under|max)\s*(\d+)", text)
    if price_match:
        filters["max_price"] = float(price_match.group(1))

    # CITY
    cities = ["nha trang", "da nang", "ho chi minh", "hanoi"]
    for city in cities:
        if city in text:
            filters["city"] = city.title()
            break

    # BEDROOMS: "2br", "2 bedrooms"
    bed_match = re.search(r"(\d+)\s*(?:br|bed|bedroom)", text)
    if bed_match:
        filters["min_bedrooms"] = int(bed_match.group(1))

    # FEATURES
    if "pool" in text:
        filters["pool"] = True

    if "sea" in text or "beach" in text:
        filters["sea_view"] = True

    if "pet" in text:
        filters["pet_friendly"] = True

    return filters

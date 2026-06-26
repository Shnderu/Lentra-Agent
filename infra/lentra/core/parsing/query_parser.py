
def parse_query(text: str):
    text = text.lower()

    return {
        "city": detect_city(text),
        "budget": extract_budget(text),
        "type": detect_type(text),
        "raw": text
    }


def detect_city(text: str):
    for city in ["da nang", "bangkok", "bali", "chiang mai"]:
        if city in text:
            return city
    return "da nang"


def extract_budget(text: str):
    # MVP: очень грубо
    import re
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else None


def detect_type(text: str):
    if "studio" in text:
        return "studio"
    if "villa" in text:
        return "villa"
    return "apartment"

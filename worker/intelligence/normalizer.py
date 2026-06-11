import re

def normalize_price(price, currency):
    if price is None:
        return None

    # базовая нормализация (расширится позже FX layer)
    return {
        "value": float(price),
        "currency": currency or "USD"
    }


def normalize_text(text: str):
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_property(item: dict) -> dict:
    return {
        "title": normalize_text(item.get("title")),
        "price": normalize_price(item.get("price"), item.get("currency")),
        "location": normalize_text(item.get("location")),
        "source": item.get("source"),
        "url": item.get("url")
    }

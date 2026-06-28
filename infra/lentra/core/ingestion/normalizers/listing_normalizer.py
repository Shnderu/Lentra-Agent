

def normalize(raw: dict) -> dict:

    return {
        "id": raw.get("id"),
        "title": raw.get("title", ""),
        "price": float(raw.get("price", 0)),
        "city": raw.get("city", ""),
        "location": raw.get("location", ""),
        "currency": raw.get("currency", "USD"),
        "source": raw.get("source", "unknown")
    }

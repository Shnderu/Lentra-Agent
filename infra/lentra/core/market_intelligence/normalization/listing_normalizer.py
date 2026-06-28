

def normalize_listing(raw):

    return {
        "id": raw.get("id"),
        "title": raw.get("title", "unknown"),
        "price": raw.get("price", 0),
        "currency": raw.get("currency", "USD"),
        "city": raw.get("city", "unknown"),
        "location": raw.get("location", ""),
        "source": raw.get("source", "unknown"),
        "features": raw.get("features", [])
    }

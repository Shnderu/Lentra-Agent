

# =========================
# RESPONSE FORMATTER v1
# =========================

def format_response(context):
    """
    Преобразует execution context в стабильный API DTO
    """

    ranked = getattr(context, "ranked", [])
    listings = getattr(context, "listings", [])
    query = getattr(context, "query", None)

    def serialize(item):
        return {
            "id": item.get("id"),
            "title": item.get("title"),
            "price": item.get("price"),
            "city": item.get("city"),
            "source": item.get("source", "unknown")
        }

    return {
        "query": getattr(query, "raw", None) if hasattr(query, "raw") else str(query),
        "count": len(ranked),
        "results": [serialize(x) for x in ranked],
        "meta": {
            "mode": "v1",
            "monetized": True if any(x.get("source") == "premium" for x in listings) else False
        }
    }

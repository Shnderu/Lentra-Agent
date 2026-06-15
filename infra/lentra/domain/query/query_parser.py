def parse_query(payload: dict) -> dict:
    """
    Минимальный стабильный parser.
    Сейчас только нормализует вход.
    """
    query = payload.get("query", "")

    return {
        "raw_query": query,
        "city": payload.get("city"),
        "budget_max": payload.get("budget_max"),
    }

from app.core.events import Event


def rent_search(query: str) -> dict:
    """
    MOCK SERVICE — пока без API / БД
    Это критическая точка будущих фейлов (latency + external dependency)
    """

    if not query:
        raise ValueError("empty query")

    # имитация внешнего ответа
    return {
        "results": [
            {"title": "Apartment A", "price": 500},
            {"title": "Apartment B", "price": 700},
        ],
        "query": query
    }

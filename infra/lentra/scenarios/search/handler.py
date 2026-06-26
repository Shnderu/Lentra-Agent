def handle(flow, params=None):
    """
    Search scenario v1

    Здесь будет:
    - маршруты
    - билеты
    - аренда
    - любая search-логика продукта
    """

    return {
        "status": "ok",
        "scenario": "search",
        "result": f"search executed for: {flow.text}"
    }

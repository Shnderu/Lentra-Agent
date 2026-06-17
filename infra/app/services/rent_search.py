import time


def rent_search(query: str) -> dict:
    if not query:
        raise ValueError("empty query")

    # имитация latency внешнего API
    time.sleep(0.15)

    return {
        "results": [
            {"title": "Apartment A", "price": 500},
            {"title": "Apartment B", "price": 700},
        ],
        "query": query
    }

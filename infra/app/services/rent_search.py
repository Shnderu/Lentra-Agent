import time
import random


def rent_search(query: str) -> dict:
    if not query:
        raise ValueError("empty query")

    # имитация нестабильного внешнего API
    if random.random() < 0.15:
        time.sleep(1.5)
        raise TimeoutError("external API timeout")

    time.sleep(0.12)

    return {
        "results": [
            {"title": "Apartment A", "price": 500},
            {"title": "Apartment B", "price": 700},
        ],
        "query": query
    }

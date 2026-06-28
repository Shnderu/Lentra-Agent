

from fastapi import FastAPI
from lentra.core.pipeline.pipeline import LentraPipeline

app = FastAPI()
pipeline = LentraPipeline()


def safe_run(raw_listing):
    result = pipeline.run(raw_listing)

    # гарантируем одинаковый формат для UI
    if "ui_badges" not in result:
        result["ui_badges"] = []

    if "ai" not in result:
        result["ai"] = {"advice": [], "warnings": [], "verdict": None}

    return result


@app.get("/search")
def search(q: str):

    raw_listing = {
        "id": "api-1",
        "title": q,
        "price": 600,
        "market_avg": 600,
        "currency": "USD",
        "city": "Da Nang",
        "location": "My My",
        "source": "api"
    }

    return {
        "query": q,
        "result": safe_run(raw_listing)
    }


@app.get("/listing")
def listing(id: str):

    raw_listing = {
        "id": id,
        "title": "studio",
        "price": 600,
        "market_avg": 550,
        "currency": "USD",
        "city": "Da Nang",
        "location": "My My",
        "source": "api"
    }

    return safe_run(raw_listing)

from fastapi import FastAPI, Query
from lentra.services.ranking_service import get_feed

app = FastAPI()


@app.get("/feed")
def feed(
    user_id: int = Query(None),
    limit: int = 10
):
    user = None

    if user_id:
        user = {
            "min_price": 0,
            "max_price": 1000,
            "prefers_sea_view": True
        }

    return get_feed(limit=limit, user=user)


@app.get("/health")
def health():
    return {"status": "ok"}

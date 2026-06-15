from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import psycopg2

from lentra.domain.property.search import search_properties
from lentra.domain.feature_store import FeatureStore

app = FastAPI()


class SearchRequest(BaseModel):
    query: str
    city: str
    budget_max: Optional[float] = None


def get_db():
    return psycopg2.connect(
        dbname="lentra",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )


@app.post("/v1/search")
def search(req: SearchRequest):

    conn = get_db()

    try:
        feature_store = FeatureStore(conn)

        state = {
            "city": req.city,
            "budget_max": req.budget_max,
            "feature_store": feature_store
        }

        results = search_properties(req.model_dump(), state)

        return {
            "results": results,
            "meta": {
                "count": len(results),
                "version": "v6.5"
            }
        }

    finally:
        conn.close()

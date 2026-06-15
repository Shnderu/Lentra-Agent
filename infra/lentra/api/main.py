from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

from lentra.data.providers.properties_provider import fetch_properties
from lentra.domain.search.ranking import rank_properties

app = FastAPI()


class SearchRequest(BaseModel):
    query: str
    city: str | None = None
    budget_max: float | None = None


def get_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "lentra"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=5432
    )


@app.post("/v1/search")
def search(req: SearchRequest):
    conn = get_db()

    try:
        props = fetch_properties(conn, req.model_dump() or {})

        if not props:
            return {"results": [], "meta": {"count": 0, "version": "v6.7-fixed"}}

        ranked = rank_properties(props, req.model_dump() or {})

        return {
            "results": ranked,
            "meta": {
                "count": len(ranked),
                "version": "v6.7-fixed"
            }
        }

    finally:
        conn.close()

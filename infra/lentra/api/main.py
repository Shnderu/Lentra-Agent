from fastapi import FastAPI
from lentra.api.db import get_db
from lentra.data.providers.properties_provider import fetch_properties

app = FastAPI()

@app.post("/v1/search")
def search(req: dict):
    conn = get_db()

    try:
        props = fetch_properties(conn, req or {})
        return {
            "results": props,
            "meta": {"count": len(props), "version": "v7-db-fixed"}
        }
    finally:
        conn.close()

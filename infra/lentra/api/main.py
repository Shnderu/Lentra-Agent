from fastapi import FastAPI, Request, Depends
from lentra.domain.query.query_parser import parse_query
from lentra.data.providers.properties_provider import fetch_properties
from lentra.db import get_db

app = FastAPI()


def db_dep():
    conn = next(get_db())
    try:
        yield conn
    finally:
        conn.close()


@app.post("/v1/search")
async def search(request: Request, conn=Depends(db_dep)):
    body = await request.json()

    query = body.get("query", "")
    budget_max = body.get("budget_max")

    parsed = parse_query(query)

    query_obj = {
        "query": query,
        "budget_max": budget_max,
        **parsed
    }

    props = fetch_properties(conn, query_obj)

    return {
        "results": props,
        "meta": {"count": len(props)}
    }

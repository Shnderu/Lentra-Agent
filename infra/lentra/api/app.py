from fastapi import FastAPI
from lentra.api.search.router import search_endpoint

app = FastAPI(title="Lentra Search API", version="1.0")


@app.post("/search")
def search(payload: dict):
    """
    External search endpoint
    """
    return search_endpoint(payload)

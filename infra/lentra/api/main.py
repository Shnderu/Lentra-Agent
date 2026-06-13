# ============================================================
# API ENTRYPOINT V17.2
# ============================================================

from fastapi import FastAPI
from lentra.api.routes.search import search_endpoint

app = FastAPI()

@app.post("/search")
async def search(request: dict):
    return await search_endpoint(request)

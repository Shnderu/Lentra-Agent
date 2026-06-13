# ============================================================
# LENTRA MVP API
# ============================================================

from fastapi import FastAPI
from lentra.core.search_service import SearchService

app = FastAPI()
service = SearchService()


@app.post("/search")
async def search(request: dict):
    return await service.search(request)

from fastapi import FastAPI
from pydantic import BaseModel

from lentra.services.intelligence import handle_request

# КРИТИЧНО: гарантируем загрузку сценариев и регистрацию в runtime
# без этого scenario_registry остаётся пустым
import lentra.scenarios


app = FastAPI()


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(request: SearchRequest):
    payload = {
        "query": request.query
    }
    return handle_request(payload)

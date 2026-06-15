from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from lentra.api.deps import get_db, get_search_service
from lentra.db.services.dto import SearchRequestDTO


app = FastAPI()


class SearchRequest(BaseModel):
    query: str
    budget_max: float | None = None


@app.post("/v1/search", response_model=None)
def search(
    req: SearchRequest,
    db: Session = Depends(get_db)
):
    service = get_search_service(db)

    result = service.search(
        SearchRequestDTO(
            query=req.query,
            budget_max=req.budget_max
        )
    )

    return result

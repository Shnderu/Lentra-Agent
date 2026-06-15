from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from lentra.db.deps import get_db
from lentra.services.search_service import SearchService

app = FastAPI()

@app.post("/v1/search")
def search(payload: dict, db: Session = Depends(get_db)):
    service = SearchService(db)

    return service.search(
        query=payload.get("query", ""),
        budget_max=payload.get("budget_max", 999)
    )

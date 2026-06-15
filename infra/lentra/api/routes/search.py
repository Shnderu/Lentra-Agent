from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lentra.api.deps import get_db
from lentra.db.repositories.apartment_repository import ApartmentRepository
from lentra.db.services.search_service import SearchService

router = APIRouter()


@router.post("/v1/search")
def search(payload: dict, db: Session = Depends(get_db)):
    query = payload.get("query")
    budget_max = payload.get("budget_max")

    repo = ApartmentRepository(db)
    service = SearchService(repo)

    return service.search(query=query, budget_max=budget_max)

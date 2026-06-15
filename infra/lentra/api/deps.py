from typing import Generator

from sqlalchemy.orm import Session

from lentra.db.session import SessionLocal
from lentra.db.repositories.apartment_repo import ApartmentRepository
from lentra.db.services.search_service import SearchService


# ------------------------
# DB SESSION (OK)
# ------------------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# SERVICE (FIXED PROPER FASTAPI WAY)
# ------------------------
def get_search_service(db: Session = None) -> SearchService:
    """
    ❗ ВАЖНО:
    db должен приходить через Depends, а не через next()
    """
    repo = ApartmentRepository(db)
    return SearchService(repo)

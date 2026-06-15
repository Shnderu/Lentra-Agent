from lentra.db.session import SessionLocal
from lentra.db.repositories.apartment_repository import ApartmentRepository
from lentra.db.services.search_service import SearchService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_search_service(db=next(get_db())):
    repo = ApartmentRepository(db)
    return SearchService(repo)

from sqlalchemy.orm import Session
from sqlalchemy import select
from lentra.db.models.apartment import Apartment


class ApartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(Apartment)
        return self.db.execute(stmt).scalars().all()

    def filter_by_city(self, city: str):
        stmt = select(Apartment).where(Apartment.city == city)
        return self.db.execute(stmt).scalars().all()

    def search_basic(self, city: str | None = None, max_price: float | None = None):
        stmt = select(Apartment)

        if city:
            stmt = stmt.where(Apartment.city.ilike(f"%{city}%"))

        if max_price is not None:
            stmt = stmt.where(Apartment.price_vnd_mln <= max_price)

        return self.db.execute(stmt).scalars().all()

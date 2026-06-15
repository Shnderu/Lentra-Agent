from sqlalchemy.orm import Session
from sqlalchemy import and_

from lentra.db.models.apartment import Apartment


class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        city: str | None = None,
        budget_max: float | None = None,
        pool: bool | None = None,
        sea_view: bool | None = None,
    ):
        query = self.db.query(Apartment)

        filters = []

        if city:
            filters.append(Apartment.city == city)

        if budget_max is not None:
            filters.append(Apartment.price_vnd_mln <= budget_max)

        if pool is not None:
            filters.append(Apartment.pool == pool)

        if sea_view is not None:
            filters.append(Apartment.sea_view == sea_view)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()

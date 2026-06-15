from sqlalchemy.orm import Session
from lentra.db.models import Apartment


class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def filter_basic(self, city=None, max_price=None, pool=None, sea_view=None):
        query = self.db.query(Apartment)

        if city:
            query = query.filter(Apartment.city == city)

        if max_price:
            query = query.filter(Apartment.price_vnd_mln <= max_price)

        if pool is not None:
            query = query.filter(Apartment.pool == pool)

        if sea_view is not None:
            query = query.filter(Apartment.sea_view == sea_view)

        return query.all()

    def get_by_id(self, apartment_id: int):
        return self.db.query(Apartment).filter(Apartment.id == apartment_id).first()

from sqlalchemy.orm import Session
from lentra.models.apartment import Apartment

class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def search(self, city=None, max_price=None):
        query = self.db.query(Apartment)

        if city:
            query = query.filter(Apartment.city == city)

        if max_price:
            query = query.filter(Apartment.price_vnd_mln <= max_price)

        return query.all()

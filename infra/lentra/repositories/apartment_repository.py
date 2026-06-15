from sqlalchemy.orm import Session
from lentra.db.models import Apartment


class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def search_all(self):
        return self.db.query(Apartment).all()

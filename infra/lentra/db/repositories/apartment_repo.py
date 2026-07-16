from typing import List

from sqlalchemy.orm import Session
from lentra.models.apartment import Apartment


class ApartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Apartment]:
        return self.db.query(Apartment).all()

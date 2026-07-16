from typing import List, Optional

from sqlalchemy.orm import Session

from lentra.models.storage import PropertyDB


class PropertyRepository:
    """
    Canonical database repository for PropertyDB.

    Responsibility:
    - SQLAlchemy access only
    - no scoring
    - no ranking
    - no market calculations
    """

    def __init__(
        self,
        db: Session
    ):
        self.db = db


    def list_all(self) -> List[PropertyDB]:
        return (
            self.db
            .query(PropertyDB)
            .all()
        )


    def search(
        self,
        city: Optional[str] = None,
        budget_max: Optional[float] = None
    ) -> List[PropertyDB]:

        query = (
            self.db
            .query(PropertyDB)
        )


        if city:

            query = query.filter(
                PropertyDB.city == city
            )


        if budget_max is not None:

            query = query.filter(
                PropertyDB.price_vnd_mln <= budget_max
            )


        return query.all()


    def get_by_id(
        self,
        property_id: int
    ) -> Optional[PropertyDB]:

        return (
            self.db
            .query(PropertyDB)
            .filter(
                PropertyDB.id == property_id
            )
            .first()
        )

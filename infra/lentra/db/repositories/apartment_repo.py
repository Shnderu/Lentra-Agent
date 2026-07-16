from typing import List, Optional

from sqlalchemy.orm import Session

from lentra.models.apartment import Apartment


class ApartmentRepository:
    """
    Canonical database repository for Apartment.

    Responsibility:
    - SQLAlchemy access only
    - no scoring
    - no business intelligence
    - no market calculations

    Business ranking belongs to upper layers.
    """

    def __init__(
        self,
        db: Session
    ):
        self.db = db


    def list_all(self) -> List[Apartment]:
        return (
            self.db
            .query(Apartment)
            .all()
        )


    def search(
        self,
        city: Optional[str] = None,
        budget_max: Optional[float] = None
    ) -> List[Apartment]:

        query = (
            self.db
            .query(Apartment)
        )


        if city:

            query = query.filter(
                Apartment.city == city
            )


        if budget_max is not None:

            query = query.filter(
                Apartment.price_vnd_mln <= budget_max
            )


        return query.all()


    def get_by_id(
        self,
        apartment_id: int
    ) -> Optional[Apartment]:

        return (
            self.db
            .query(Apartment)
            .filter(
                Apartment.id == apartment_id
            )
            .first()
        )

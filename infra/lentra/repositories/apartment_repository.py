from sqlalchemy import text
from sqlalchemy.orm import Session
from .base import BaseRepository


class ApartmentRepository(BaseRepository):

    def search_candidates(self, city: str | None = None):
        """
        Базовая выборка кандидатов из БД
        (без scoring, без бизнес-логики)
        """

        query = """
        SELECT
            id,
            title,
            price_vnd_mln,
            area_m2,
            bedrooms,
            bathrooms,
            pet_friendly,
            pool,
            sea_view,
            city,
            district
        FROM apartments
        WHERE 1=1
        """

        params = {}

        if city:
            query += " AND city = :city"
            params["city"] = city

        return self.db.execute(text(query), params).mappings().all()

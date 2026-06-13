from sqlalchemy import create_engine, text
import os

from lentra.services.ranking_service import RankingService

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

ranking = RankingService()


class SearchService:

    # ----------------------------
    # MAIN SEARCH
    # ----------------------------
    def search(
        self,
        location: str = None,
        max_price: float = None,
        min_price: float = None,
        property_type: str = None,
        min_confidence: float = 0.3,
        limit: int = 20
    ):

        query = """
            SELECT
                id,
                description,
                price,
                currency,
                location,
                property_type,
                confidence,
                created_at
            FROM properties
            WHERE confidence >= :min_confidence
        """

        params = {
            "min_confidence": min_confidence
        }

        if location:
            query += " AND location = :location"
            params["location"] = location

        if property_type:
            query += " AND property_type = :property_type"
            params["property_type"] = property_type

        if max_price:
            query += " AND price <= :max_price"
            params["max_price"] = max_price

        if min_price:
            query += " AND price >= :min_price"
            params["min_price"] = min_price

        with engine.begin() as conn:
            rows = conn.execute(text(query), params).fetchall()

        # ----------------------------
        # reuse ranking engine
        # ----------------------------
        scored = []

        for r in rows:
            score = ranking._calculate_score(r, None)
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            {
                "id": r.id,
                "description": r.description,
                "price": r.price,
                "currency": r.currency,
                "location": r.location,
                "type": r.property_type,
                "confidence": r.confidence
            }
            for score, r in scored[:limit]
        ]

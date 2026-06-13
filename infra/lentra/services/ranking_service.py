from sqlalchemy import create_engine, text
import os
import time

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class RankingService:

    def get_feed(
        self,
        limit: int = 20,
        min_confidence: float = 0.3,
        min_bedrooms: int = None,
        max_price: float = None,
        sea_view: bool = None
    ):
        query = """
            SELECT
                id,
                title,
                price_vnd_mln,
                deposit_vnd_mln,
                area_m2,
                bedrooms,
                bathrooms,
                pet_friendly,
                pool,
                sea_view
            FROM properties
            WHERE 1=1
        """

        params = {
            "min_confidence": min_confidence
        }

        # ----------------------------
        # FILTERS
        # ----------------------------
        if min_bedrooms is not None:
            query += " AND bedrooms >= :min_bedrooms"
            params["min_bedrooms"] = min_bedrooms

        if max_price is not None:
            query += " AND price_vnd_mln <= :max_price"
            params["max_price"] = max_price

        if sea_view is not None:
            query += " AND sea_view = :sea_view"
            params["sea_view"] = sea_view

        with engine.begin() as conn:
            rows = conn.execute(text(query), params).fetchall()

        scored = []

        for r in rows:
            score = self._score(r)
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [self._format(r) for score, r in scored[:limit]]

    # ----------------------------
    # SCORING MODEL (REAL ESTATE LOGIC)
    # ----------------------------
    def _score(self, r):
        score = 0.0

        # 1. size quality
        if r.area_m2:
            if r.area_m2 > 60:
                score += 0.2
            elif r.area_m2 > 35:
                score += 0.1

        # 2. bedrooms
        if r.bedrooms:
            if r.bedrooms >= 2:
                score += 0.2
            elif r.bedrooms == 1:
                score += 0.1

        # 3. amenities boost
        if r.sea_view:
            score += 0.25

        if r.pool:
            score += 0.15

        if r.pet_friendly:
            score += 0.1

        # 4. price attractiveness (VND mln)
        if r.price_vnd_mln:
            if r.price_vnd_mln < 10:
                score += 0.2
            elif r.price_vnd_mln < 20:
                score += 0.1

        return round(score, 4)

    # ----------------------------
    # FORMAT OUTPUT
    # ----------------------------
    def _format(self, r):
        features = []

        if r.sea_view:
            features.append("sea view")
        if r.pool:
            features.append("pool")
        if r.pet_friendly:
            features.append("pet friendly")

        return {
            "id": r.id,
            "title": r.title,
            "price_vnd_mln": r.price_vnd_mln,
            "deposit_vnd_mln": r.deposit_vnd_mln,
            "area_m2": r.area_m2,
            "bedrooms": r.bedrooms,
            "bathrooms": r.bathrooms,
            "features": features
        }

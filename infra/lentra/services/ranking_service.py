from sqlalchemy import create_engine, text
import os
import time

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class RankingService:
    """
    V2 ranking engine with scoring model
    """

    # ----------------------------
    # MAIN FEED
    # ----------------------------
    def get_feed(
        self,
        limit: int = 20,
        min_confidence: float = 0.3,
        location: str = None,
        max_price: float = None
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
                EXTRACT(EPOCH FROM NOW() - created_at) as age_seconds
            FROM properties
            WHERE confidence >= :min_confidence
        """

        params = {
            "min_confidence": min_confidence
        }

        if location:
            query += " AND location = :location"
            params["location"] = location

        if max_price:
            query += " AND price <= :max_price"
            params["max_price"] = max_price

        with engine.begin() as conn:
            rows = conn.execute(text(query), params).fetchall()

        scored = []

        now = time.time()

        for r in rows:
            score = self._calculate_score(r, now)
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            self._format(r)
            for score, r in scored[:limit]
        ]

    # ----------------------------
    # SCORING MODEL (CORE)
    # ----------------------------
    def _calculate_score(self, r, now):
        score = 0.0

        # 1. base confidence
        score += (r.confidence or 0) * 0.6

        # 2. freshness boost (new = better)
        age_hours = (r.age_seconds or 0) / 3600

        if age_hours < 6:
            score += 0.25
        elif age_hours < 24:
            score += 0.15
        elif age_hours < 72:
            score += 0.05

        # 3. price quality boost (cheap = better signal in SEA context)
        if r.price:
            if r.price < 300:
                score += 0.15
            elif r.price < 600:
                score += 0.10
            elif r.price < 1000:
                score += 0.05

        # 4. completeness boost
        completeness = 0.0

        if r.location:
            completeness += 0.1
        if r.property_type:
            completeness += 0.1
        if r.price:
            completeness += 0.1

        score += completeness

        return round(score, 4)

    # ----------------------------
    # FORMAT OUTPUT
    # ----------------------------
    def _format(self, r):
        return {
            "id": r.id,
            "description": r.description,
            "price": r.price,
            "currency": r.currency,
            "location": r.location,
            "type": r.property_type,
            "confidence": r.confidence
        }

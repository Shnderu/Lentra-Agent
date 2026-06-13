from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_user_affinity(user_id: int):
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT property_id, SUM(weight) as score
            FROM user_feedback
            WHERE user_id = :user_id
            GROUP BY property_id
        """), {"user_id": user_id}).fetchall()

    return {r.property_id: r.score for r in rows}

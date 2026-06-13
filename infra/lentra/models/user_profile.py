from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL)


def get_user_profile(user_id: int):
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT *
            FROM user_profiles
            WHERE user_id = :user_id
        """), {"user_id": user_id}).fetchone()

        return row


def create_default_profile(user_id: int):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO user_profiles (user_id, min_price, max_price, prefers_sea_view)
            VALUES (:user_id, 0, 999999, false)
            ON CONFLICT (user_id) DO NOTHING
        """), {"user_id": user_id})

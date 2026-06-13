from sqlalchemy import create_engine, text
import os

engine = create_engine(
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)


def get_user_profile(user_id: int):
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT *
            FROM user_profiles
            WHERE user_id = :user_id
        """), {"user_id": user_id}).fetchone()

    return row

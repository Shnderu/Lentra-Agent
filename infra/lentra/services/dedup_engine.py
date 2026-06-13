from sqlalchemy import create_engine, text
import os
import hashlib

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def make_hash(user_id: int, property_id: int):
    return hashlib.md5(f"{user_id}:{property_id}".encode()).hexdigest()


def was_sent(user_id: int, property_id: int):
    h = make_hash(user_id, property_id)

    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT 1 FROM user_feedback
            WHERE user_id = :user_id
              AND property_id = :property_id
              AND event_type = 'sent'
        """), {
            "user_id": user_id,
            "property_id": property_id
        }).fetchone()

    return row is not None


def mark_sent(user_id: int, property_id: int):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO user_feedback (user_id, property_id, event_type, weight)
            VALUES (:user_id, :property_id, 'sent', 1)
        """), {
            "user_id": user_id,
            "property_id": property_id
        })

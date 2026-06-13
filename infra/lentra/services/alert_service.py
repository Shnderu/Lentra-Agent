from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class AlertService:

    # ----------------------------
    # CREATE ALERT
    # ----------------------------
    def create_alert(self, chat_id, location=None, max_price=None):
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO alerts (chat_id, location, max_price)
                VALUES (:chat_id, :location, :max_price)
            """), {
                "chat_id": chat_id,
                "location": location,
                "max_price": max_price
            })

    # ----------------------------
    # GET ALERTS
    # ----------------------------
    def get_active_alerts(self):
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT id, chat_id, location, max_price, min_confidence
                FROM alerts
                WHERE is_active = TRUE
            """)).fetchall()

        return rows

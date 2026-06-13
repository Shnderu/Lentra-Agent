from sqlalchemy import create_engine, text
import os

from lentra.services.alert_service import AlertService

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

alerts = AlertService()


class AlertMatcher:

    # ----------------------------
    # GET MATCHES (DEDUP ENABLED)
    # ----------------------------
    def get_new_matches(self):
        alert_list = alerts.get_active_alerts()
        results = []

        for alert in alert_list:
            alert_id, chat_id, location, max_price, min_conf = alert

            query = """
                SELECT id, description, price, currency, location, confidence
                FROM properties p
                WHERE p.confidence >= :min_conf
            """

            params = {"min_conf": min_conf}

            if location:
                query += " AND p.location = :location"
                params["location"] = location

            if max_price:
                query += " AND p.price <= :max_price"
                params["max_price"] = max_price

            # IMPORTANT: exclude already sent properties
            query += """
                AND NOT EXISTS (
                    SELECT 1 FROM alert_matches am
                    WHERE am.alert_id = :alert_id
                    AND am.property_id = p.id
                )
                ORDER BY p.id DESC
                LIMIT 5
            """

            params["alert_id"] = alert_id

            with engine.begin() as conn:
                rows = conn.execute(text(query), params).fetchall()

            for r in rows:
                results.append((alert_id, chat_id, r))

        return results

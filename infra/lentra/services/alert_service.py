from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL)


def match_alerts(property_row):
    with engine.begin() as conn:
        alerts = conn.execute(text("""
            SELECT user_id, min_price, max_price
            FROM user_profiles
        """)).fetchall()

    matches = []

    for a in alerts:
        if property_row.price_vnd_mln is None:
            continue

        if a.min_price <= property_row.price_vnd_mln <= a.max_price:
            matches.append(a.user_id)

    return matches

from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def find_matching_users(property_data):
    with engine.begin() as conn:
        users = conn.execute(text("""
            SELECT user_id, min_price, max_price, prefers_sea_view
            FROM user_profiles
        """)).fetchall()

    matches = []

    for u in users:
        if property_data.price_vnd_mln is None:
            continue

        if not (u.min_price <= property_data.price_vnd_mln <= u.max_price):
            continue

        if u.prefers_sea_view and not property_data.sea_view:
            continue

        matches.append(u.user_id)

    return matches

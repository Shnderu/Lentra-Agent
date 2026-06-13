from sqlalchemy import create_engine, text
from lentra.domain.property import Property
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_property_by_raw_message(raw_message_id: int):
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT *
            FROM properties
            WHERE id = (
                SELECT id FROM properties ORDER BY id DESC LIMIT 1
            )
            LIMIT 1
        """)).fetchone()

    if not row:
        return None

    return Property(
        id=row.id,
        title=row.title,
        price_vnd_mln=row.price_vnd_mln,
        area_m2=row.area_m2,
        bedrooms=row.bedrooms,
        bathrooms=row.bathrooms,
        pet_friendly=row.pet_friendly,
        pool=row.pool,
        sea_view=row.sea_view
    )

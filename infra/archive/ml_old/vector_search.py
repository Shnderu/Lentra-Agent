from sqlalchemy import create_engine, text
import os

from lentra.ml.embeddings import embed

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def search(query: str, limit: int = 20):
    qvec = embed(query)

    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT property_id,
                   embedding <=> :vec AS distance
            FROM property_embeddings
            ORDER BY embedding <=> :vec
            LIMIT :limit
        """), {
            "vec": qvec,
            "limit": limit
        }).fetchall()

    return [r.property_id for r in rows]

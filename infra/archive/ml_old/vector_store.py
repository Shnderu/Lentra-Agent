from sqlalchemy import create_engine, text
import os

from lentra.ml.embeddings import embed

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def upsert_property_embedding(property_id: int, text: str):
    vec = embed(text)

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO property_embeddings (property_id, embedding)
            VALUES (:id, :embedding)
            ON CONFLICT (property_id)
            DO UPDATE SET embedding = EXCLUDED.embedding, updated_at = NOW()
        """), {
            "id": property_id,
            "embedding": vec
        })

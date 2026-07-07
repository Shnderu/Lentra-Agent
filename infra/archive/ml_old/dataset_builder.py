from sqlalchemy import create_engine, text
import os
import pandas as pd

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def build_dataset():
    with engine.begin() as conn:
        df = pd.read_sql(text("""
            SELECT
                p.id,
                p.price_vnd_mln,
                p.area_m2,
                p.bedrooms,
                p.bathrooms,
                p.pool,
                p.sea_view,
                COALESCE(SUM(f.weight), 0) AS label
            FROM properties p
            LEFT JOIN user_feedback f
                ON p.id = f.property_id
            GROUP BY p.id
        """), conn)

    return df


if __name__ == "__main__":
    df = build_dataset()
    df.to_csv("/opt/lentra/infra/lentra/ml/dataset.csv", index=False)
    print("[ML] dataset built:", len(df))

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL)

def run():
    with engine.begin() as conn:
        stats = conn.execute(text("""
            SELECT status, COUNT(*)
            FROM processing_queue
            GROUP BY status
        """)).fetchall()

        raw = conn.execute(text("""
            SELECT COUNT(*) FROM raw_messages
        """)).fetchone()[0]

        props = conn.execute(text("""
            SELECT COUNT(*) FROM properties
        """)).fetchone()[0]

    print("\n=== PIPELINE STATUS ===")
    print("RAW MESSAGES:", raw)
    print("PROPERTIES:", props)
    print("\nQUEUE:")
    for s, c in stats:
        print(f"  {s}: {c}")

if __name__ == "__main__":
    run()

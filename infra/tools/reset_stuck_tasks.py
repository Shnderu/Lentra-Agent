from sqlalchemy import text

from lentra.db.session import SessionLocal

STALE_MINUTES = 10

db = SessionLocal()

try:
    result = db.execute(
        text(
            """
            UPDATE processing_queue
            SET
                status='pending',
                updated_at=NOW()
            WHERE
                status='processing'
                AND updated_at < NOW() - INTERVAL '10 minutes'
            """
        )
    )

    db.commit()

    print(f"[RESET] restored {result.rowcount} stuck tasks")

finally:
    db.close()

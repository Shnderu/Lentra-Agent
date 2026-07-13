from typing import Generator

from sqlalchemy.orm import Session

from lentra.db.session import SessionLocal


# ------------------------
# DB SESSION
# ------------------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

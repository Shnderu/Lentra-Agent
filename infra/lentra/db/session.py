import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    (
        "postgresql://"
        f"{os.getenv('LENTRA_DB_USER', 'lentra')}:"
        f"{os.getenv('LENTRA_DB_PASSWORD', 'lentra')}@"
        f"{os.getenv('LENTRA_DB_HOST', '127.0.0.1')}:"
        f"{os.getenv('LENTRA_DB_PORT', '5432')}/"
        f"{os.getenv('LENTRA_DB_NAME', 'lentra')}"
    ),
)


engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
